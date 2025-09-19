import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function JobList() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("All");
  const [sort, setSort] = useState("application_date");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/job-applications/")
      .then((res) => res.json())
      .then((data) => setJobs(data))
      .catch((err) => console.error("Error fetching jobs:", err));
  }, []);

  const filteredJobs = jobs
    .filter((job) =>
      search
        ? job.company_name.toLowerCase().includes(search.toLowerCase()) ||
          job.position.toLowerCase().includes(search.toLowerCase())
        : true
    )
    .filter((job) => (status === "All" ? true : job.status === status))
    .sort((a, b) => {
      if (sort === "application_date") {
        return new Date(b.application_date) - new Date(a.application_date);
      }
      if (sort === "company_name") {
        return a.company_name.localeCompare(b.company_name);
      }
      return 0;
    });

  return (
    <div className="container">
      <h1 className="mb-4">Job Applications</h1>

      {/* Filter + Sort Form */}
      <div className="d-flex flex-wrap mb-3 gap-2">
        <input
          type="text"
          placeholder="Search jobs..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="form-control"
          style={{ maxWidth: "250px" }}
        />

        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="form-select"
        >
          <option value="All">All</option>
          <option value="Applied">Applied</option>
          <option value="Interview">Interview</option>
          <option value="Offer">Offer</option>
          <option value="Rejected">Rejected</option>
        </select>

        <select
          value={sort}
          onChange={(e) => setSort(e.target.value)}
          className="form-select"
        >
          <option value="application_date">Date</option>
          <option value="company_name">Company</option>
        </select>
      </div>

      {/* Jobs Table */}
      {filteredJobs.length > 0 ? (
        <div className="table-responsive">
          <table className="table table-bordered table-striped">
            <thead className="table-dark">
              <tr>
                <th>Company</th>
                <th>Position</th>
                <th>Applied On</th>
                <th>Status</th>
                <th>Resume</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredJobs.map((job) => (
                <tr key={job.id}>
                  <td>{job.company_name}</td>
                  <td>{job.position}</td>
                  <td>{job.application_date}</td>
                  <td>{job.status}</td>
                  <td>
                    {job.resume ? (
                      <a
                        href={job.resume}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        Download
                      </a>
                    ) : (
                      "N/A"
                    )}
                  </td>
                  <td>
                    <Link
                      to={`/job/${job.id}`}
                      className="btn btn-info btn-sm"
                    >
                      View
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="alert alert-warning">No job applications found.</div>
      )}
    </div>
  );
}

export default JobList;