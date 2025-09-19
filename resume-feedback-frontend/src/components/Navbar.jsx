import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar navbar-dark bg-dark mb-4">
      <div className="container-fluid d-flex justify-content-between">
        <Link className="navbar-brand" to="/">
          AI Job Tracker
        </Link>
        <div className="d-flex gap-3">
          <Link className="nav-link text-light" to="/analytics">
            📊 Analytics
          </Link>
          <Link className="nav-link text-light" to="/add">
            ➕ Add Job
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;