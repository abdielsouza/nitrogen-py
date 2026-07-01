use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyString, PyInt, PyFloat, PyBool};

#[derive(Debug, Clone)]
pub enum Value {
    None,
    Bool(bool),
    Int(i64),
    Float(f64),
    String(String),
}

impl IntoPy<PyObject> for Value {
    fn into_py(self, py: Python<'_>) -> PyObject {
        match self {
            Value::None => py.None(),
            Value::Bool(b) => b.into_py(py),
            Value::Int(i) => i.into_py(py),
            Value::Float(f) => f.into_py(py),
            Value::String(s) => s.into_py(py),
        }
    }
}

impl<'source> FromPyObject<'source> for Value {
    fn extract_bound(ob: &Bound<'source, PyAny>) -> PyResult<Self> {
        if ob.is_none() {
            Ok(Value::None)
        } else if let Ok(b) = ob.downcast::<PyBool>() {
            Ok(Value::Bool(b.is_true()))
        } else if let Ok(i) = ob.downcast::<PyInt>() {
            Ok(Value::Int(i.extract()?))
        } else if let Ok(f) = ob.downcast::<PyFloat>() {
            Ok(Value::Float(f.extract()?))
        } else if let Ok(s) = ob.downcast::<PyString>() {
            Ok(Value::String(s.to_string()))
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>("Unsupported type for Value"))
        }
    }
}
