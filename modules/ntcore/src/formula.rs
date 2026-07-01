use pyo3::prelude::*;

#[pyclass]
pub struct Formula;

#[pymethods]
impl Formula {
    #[new]
    pub fn new() -> Self {
        Formula
    }
}
