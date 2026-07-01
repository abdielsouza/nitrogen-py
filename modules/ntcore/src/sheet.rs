use pyo3::prelude::*;

#[pyclass]
pub struct Sheet {
    pub name: Option<String>,
}

#[pymethods]
impl Sheet {
    #[new]
    #[pyo3(signature = (name = None))]
    pub fn new(name: Option<String>) -> Self {
        Sheet { name }
    }
}
