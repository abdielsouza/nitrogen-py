use pyo3::prelude::*;
use pyo3::types::{PyAny, PySet};

#[derive(Clone)]
pub enum ExpressionKind {
    Reference(String),
    Add(Py<Expression>, Py<Expression>),
    Subtract(Py<Expression>, Py<Expression>),
    Multiply(Py<Expression>, Py<Expression>),
    Divide(Py<Expression>, Py<Expression>),
}

#[pyclass]
#[derive(Clone)]
pub struct Expression {
    pub kind: ExpressionKind,
}

#[pymethods]
impl Expression {
    #[staticmethod]
    pub fn reference(name: String) -> Self {
        Expression {
            kind: ExpressionKind::Reference(name),
        }
    }

    pub fn dependencies<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PySet>> {
        let set = PySet::new(py, &[])?;
        self.collect_dependencies(py, set.clone())?;
        Ok(set)
    }

    pub fn compile(&self, _backend: Option<Bound<'_, PyAny>>) -> PyResult<String> {
        Ok("compiled".to_string())
    }

    fn __repr__(&self, py: Python<'_>) -> PyResult<String> {
        Ok(self.to_string(py))
    }

    fn __add__(&self, other: Bound<'_, PyAny>, py: Python<'_>) -> PyResult<Expression> {
        let right = Expression::from_any(&other, py)?;
        Ok(Expression {
            kind: ExpressionKind::Add(self.clone().into_py(py), right.into_py(py)),
        })
    }

    fn __sub__(&self, other: Bound<'_, PyAny>, py: Python<'_>) -> PyResult<Expression> {
        let right = Expression::from_any(&other, py)?;
        Ok(Expression {
            kind: ExpressionKind::Subtract(self.clone().into_py(py), right.into_py(py)),
        })
    }

    fn __mul__(&self, other: Bound<'_, PyAny>, py: Python<'_>) -> PyResult<Expression> {
        let right = Expression::from_any(&other, py)?;
        Ok(Expression {
            kind: ExpressionKind::Multiply(self.clone().into_py(py), right.into_py(py)),
        })
    }

    fn __truediv__(&self, other: Bound<'_, PyAny>, py: Python<'_>) -> PyResult<Expression> {
        let right = Expression::from_any(&other, py)?;
        Ok(Expression {
            kind: ExpressionKind::Divide(self.clone().into_py(py), right.into_py(py)),
        })
    }
}

impl Expression {
    fn collect_dependencies<'py>(&self, py: Python<'py>, set: Bound<'py, PySet>) -> PyResult<()> {
        match &self.kind {
            ExpressionKind::Reference(name) => {
                set.add(name)?;
            }
            ExpressionKind::Add(left, right)
            | ExpressionKind::Subtract(left, right)
            | ExpressionKind::Multiply(left, right)
            | ExpressionKind::Divide(left, right) => {
                if let Ok(left_expr) = left.bind(py).downcast::<Expression>() {
                    left_expr.collect_dependencies(py, set.clone())?;
                }
                if let Ok(right_expr) = right.bind(py).downcast::<Expression>() {
                    right_expr.collect_dependencies(py, set)?;
                }
            }
        }
        Ok(())
    }

    pub fn to_string(&self, _py: Python<'_>) -> String {
        match &self.kind {
            ExpressionKind::Reference(name) => format!("Reference({})", name),
            _ => "Expression".to_string(),
        }
    }

    fn from_any(other: &Bound<'_, PyAny>, py: Python<'_>) -> PyResult<Expression> {
        if let Ok(expr) = other.extract::<PyRef<Expression>>() {
            Ok(expr.clone())
        } else if let Ok(basic) = other.extract::<PyRef<BasicReference>>() {
            basic.clone().into_expression(py)
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                "Unsupported operand for expression operation",
            ))
        }
    }
}

#[pyclass]
#[derive(Clone)]
pub struct BasicReference {
    #[pyo3(get)]
    pub name: String,
    expr: Py<Expression>,
}

#[pymethods]
impl BasicReference {
    #[new]
    pub fn new(column: Bound<'_, PyAny>, py: Python<'_>) -> PyResult<Self> {
        let name: String = column.getattr("name")?.extract()?;
        let expr = Expression::reference(name.clone());
        Ok(BasicReference {
            name,
            expr: Py::new(py, expr)?,
        })
    }

    pub fn dependencies<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PySet>> {
        self.expr.bind(py).downcast::<Expression>()?.dependencies(py)
    }

    pub fn __repr__(&self) -> PyResult<String> {
        Ok(format!("Reference({})", self.name))
    }

    fn __add__(&self, other: Bound<'_, PyAny>, py: Python<'_>) -> PyResult<Expression> {
        let left = self.clone().into_expression(py)?;
        let right = Expression::from_any(&other, py)?;
        Ok(Expression {
            kind: ExpressionKind::Add(left.into_py(py), right.into_py(py)),
        })
    }

    fn __sub__(&self, other: Bound<'_, PyAny>, py: Python<'_>) -> PyResult<Expression> {
        let left = self.clone().into_expression(py)?;
        let right = Expression::from_any(&other, py)?;
        Ok(Expression {
            kind: ExpressionKind::Subtract(left.into_py(py), right.into_py(py)),
        })
    }

    fn __mul__(&self, other: Bound<'_, PyAny>, py: Python<'_>) -> PyResult<Expression> {
        let left = self.clone().into_expression(py)?;
        let right = Expression::from_any(&other, py)?;
        Ok(Expression {
            kind: ExpressionKind::Multiply(left.into_py(py), right.into_py(py)),
        })
    }

    fn __truediv__(&self, other: Bound<'_, PyAny>, py: Python<'_>) -> PyResult<Expression> {
        let left = self.clone().into_expression(py)?;
        let right = Expression::from_any(&other, py)?;
        Ok(Expression {
            kind: ExpressionKind::Divide(left.into_py(py), right.into_py(py)),
        })
    }
}

impl BasicReference {
    pub fn new_from_name(name: String, py: Python<'_>) -> PyResult<Self> {
        let expr = Expression::reference(name.clone());
        Ok(BasicReference {
            name,
            expr: Py::new(py, expr)?,
        })
    }

    pub fn into_expression(&self, _py: Python<'_>) -> PyResult<Expression> {
        Ok(Expression::reference(self.name.clone()))
    }
}
