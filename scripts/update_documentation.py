import re
from pathlib import Path
from typing import Set

from pydantic import BaseModel

from mztab_m_io import MzTabM
from mztab_m_io.model.field_utils import get_field_type_info
from mztab_m_io.model.mztabm_validation import MessageTypeMap
from mztab_m_io.model.serialization import ValidationProfile
from mztab_m_io.model.validation import MessageType


def escape_markdown(text: str) -> str:
    """
    Escape markdown special characters so they render as literal text.
    Covers headings, bold, italics, links, tables, lists, code, etc.
    """
    if not isinstance(text, str):
        return text

    # All markdown special characters
    markdown_chars = r"([\\`*_{}[\]()#+\-.!|>])"

    # Escape them by prefixing with backslash
    return re.sub(markdown_chars, r"\\\1", text)


def remove_extra_spaces(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\n +", "\n", text).strip()


def update_documentation(
    model_class: type[BaseModel], updated_documents: Set[type[BaseModel]]
):
    if model_class.__name__ in updated_documents:
        return
    model_documentation_path.mkdir(parents=True, exist_ok=True)

    md_doc_path = model_documentation_path / f"{Path(model_class.__name__)}.md"
    new_model_classes: Set[type[BaseModel]] = set()
    with md_doc_path.open("w") as f:
        f.write(f"# {model_class.__name__}\n\n")

        # f.write("## Properties\n\n")
        # add class description
        class_doc = remove_extra_spaces(model_class.__doc__)
        if class_doc:
            f.write(class_doc)
            f.write("\n\n")
        if model_class.__mztab_example__:
            f.write("## Example\n\n")
            f.write("<code>" + model_class.__mztab_example__ + "</code>")
            f.write("\n\n")
        f.write("## Properties\n\n")
        f.write(
            "|"
            + "|".join(["Name (Alias)", "Type (Default)", "Constraints", "Description"])
            + "|\n"
        )
        f.write("|" + "|".join(["---", "---", "----", "----------"]) + "|\n")

        for field, field_info in model_class.model_fields.items():
            extra = field_info.json_schema_extra or {}
            alias = field_info.validation_alias or field
            validation_profile = ValidationProfile.model_validate(extra, by_alias=True)
            is_list, field_type = get_field_type_info(model_class, field)
            name = field if field == alias else f"{field}<br/>({alias})"
            if (
                issubclass(field_type, BaseModel)
                and field_type.__name__ not in updated_documents
            ):
                new_model_classes.add(field_type)

            field_type_name = (
                f"List of <code>{field_type.__name__}</code>"
                if is_list
                else f"<code>{field_type.__name__}</code>"
            )
            default_value = field_info.default if field_info.default else ""
            if default_value:
                field_type_name = (
                    f"<code>{field_type_name}</code> (<code>{default_value}</code>)"
                )
            policy = validation_profile.validation_policy
            constraints_list = []
            if policy.required:
                constraints_list.append("**required**")
            if policy.pattern:
                constraints_list.append(
                    f"pattern: <code>{escape_markdown(policy.pattern)}</code>"
                )
            if policy.minimum:
                constraints_list.append(f"min: {policy.minimum}")
            if policy.maximum:
                constraints_list.append(f"max: {policy.maximum}")
            if policy.value_constraint:
                constraints_list.append(
                    f"format: <code>{policy.value_constraint}</code>"
                )
            constraints = "-"
            if constraints_list:
                validation_type = MessageTypeMap.get(
                    policy.enforcement_level, MessageType.ERROR
                ).value
                constraints_list.append(
                    f"Validation type: **<code>{validation_type}</code>**"
                )
                constraints = "<br/>".join(constraints_list)
            description = field_info.description or ""
            description = escape_markdown(description.replace("\n", "<br/>"))
            f.write("|".join([name, field_type_name, constraints, description]) + "\n")
        updated_documents.add(model_class.__name__)
        for new_model in new_model_classes:
            update_documentation(new_model, updated_documents)


if __name__ == "__main__":
    docs_root_path = "./docs"
    model_documentation_folder = "model"

    model_documentation_path = Path(docs_root_path) / Path(model_documentation_folder)
    updated_documents = set()
    update_documentation(MzTabM, updated_documents)
    models = list(updated_documents)
    models.sort()

    md_index_path = docs_root_path / Path("index.md")
    with md_index_path.open("w") as f:
        f.write("# mzTab-M Python Implementation\n\n")
        f.write("|" + "|".join(["Model", "Link"]) + "|\n")
        f.write("|" + "|".join(["---", "---"]) + "|\n")
        for model in models:
            f.write("|".join([model, f"[Link](model/{model}.md)"]) + "\n")
