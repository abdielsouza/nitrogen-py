use pyo3::prelude::*;

#[pyclass]
#[derive(Clone)]
pub struct DependencyGraph;

#[pymethods]
impl DependencyGraph {
    #[new]
    pub fn new() -> Self {
        DependencyGraph
    }
}

#[pyclass]
#[derive(Clone)]
pub struct GraphNode;

#[pymethods]
impl GraphNode {
    #[new]
    pub fn new() -> Self {
        GraphNode
    }
}
