use pyo3::prelude::*;

#[pyclass]
pub struct Record;

#[pymethods]
impl Record {
    #[new]
    pub fn new() -> Self {
        Record
    }
}
