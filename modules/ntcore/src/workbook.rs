use pyo3::prelude::*;

#[pyclass]
pub struct Workbook;

#[pymethods]
impl Workbook {
    #[new]
    pub fn new() -> Self {
        Workbook
    }
}
