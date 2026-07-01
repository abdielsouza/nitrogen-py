use pyo3::prelude::*;

#[pyclass]
pub struct Registry;

#[pymethods]
impl Registry {
    #[new]
    pub fn new() -> Self {
        Registry
    }
}
