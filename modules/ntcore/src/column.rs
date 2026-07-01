use pyo3::prelude::*;

#[pyclass]
pub struct Column {
    pub name: String,
}

#[pymethods]
impl Column {
    #[new]
    pub fn new(name: String) -> Self {
        Column { name }
    }
}
