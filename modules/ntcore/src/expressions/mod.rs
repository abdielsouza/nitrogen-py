use pyo3::prelude::*;

#[pyclass]
#[derive(Clone)]
pub struct Expression;

#[pymethods]
impl Expression {
    #[new]
    pub fn new() -> Self {
        Expression
    }
}

#[pyclass]
#[derive(Clone)]
pub struct BasicReference;

#[pymethods]
impl BasicReference {
    #[new]
    pub fn new() -> Self {
        BasicReference
    }
}
