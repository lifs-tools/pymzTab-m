package mztabm.utils

import rego.v1

normalize_array(value) := value if is_array(value)

normalize_array(value) := [] if not is_array(value)

get_normalized_object_array(container, property) := normalize_array(object.get(container, property, null))
