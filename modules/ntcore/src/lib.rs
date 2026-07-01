use pyo3::prelude::*;

mod column;
mod formula;
mod record;
mod relationship;
mod registry;
mod sheet;
mod workbook;
mod expressions;
mod graph;

pub use column::Column;
pub use formula::Formula;
pub use record::Record;
pub use relationship::Relationship;
pub use registry::Registry;
pub use sheet::Sheet;
pub use workbook::Workbook;
pub use expressions::{Expression, BasicReference};
pub use graph::{DependencyGraph, GraphNode};

#[pyfunction]
fn add(a: usize, b: usize) -> usize {
    a + b
}

#[pymodule]
fn ntcore(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    m.add_class::<Column>()?;
    m.add_class::<Formula>()?;
    m.add_class::<Record>()?;
    m.add_class::<Relationship>()?;
    m.add_class::<Registry>()?;
    m.add_class::<Sheet>()?;
    m.add_class::<Workbook>()?;
    m.add_class::<Expression>()?;
    m.add_class::<BasicReference>()?;
    m.add_class::<DependencyGraph>()?;
    m.add_class::<GraphNode>()?;
    Ok(())
}
