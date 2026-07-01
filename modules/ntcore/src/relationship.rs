use pyo3::prelude::*;

#[pyclass]
pub struct Relationship;

#[pymethods]
impl Relationship {
    #[new]
    pub fn new() -> Self {
        Relationship
    }
}
