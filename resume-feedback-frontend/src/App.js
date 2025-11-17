import React, { useState, useEffect } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";

function App() {
   // Auth
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("access_token")
  );

  const [view, setView] = useState("manual"); // manual or jobs

  // For manual resume feedback
  const [resumeText, setResumeText] = useState("");
  const [jobPost, setJobPost] = useState("");
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);
  

  // For job applications
  const [jobs, setJobs] = useState([]);

// Handle Login
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:8000/api/auth/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username,password }),
      });

      if (!res.ok) throw new Error("Invalid credentials");

      const data = await res.json();
      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);
      setIsLoggedIn(true);
    } catch (err) {
      alert(err.message);
    }
  };

  // Handle Logout 
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setIsLoggedIn(false);
  };

  // Fetch job data from Django
  useEffect(() => {
  if (view === "jobs" && isLoggedIn) {

    console.log("isLoggedIn:", isLoggedIn);
    console.log(" Token from localStorage:", localStorage.getItem("access_token"));

    const fetchJobs = async () => {
      try {
        setJobs([]); // Clear previous jobs

        const token = localStorage.getItem("access_token");

        const res = await fetch("http://127.0.0.1:8000/api/job-applications/", {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (res.status === 401) throw new Error("Unauthorized! Please login.");

        const data = await res.json();
        console.log("Jobs fetched:", data); // shows EXACT response from backend
        setJobs(data);

      } catch (err) {
        console.error("Error loading jobs:", err);
        setJobs([]); // Clear jobs on error
      }
    };

    fetchJobs();
  }
}, [view, isLoggedIn]);



  //  Submit Manual Resume Feedback
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setFeedback("");

    try {
      const response = await fetch("http://127.0.0.1:8000/api/get-resume-feedback/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        // ✅ include both resume_text and job_post
        body: JSON.stringify({
          resume_text: resumeText,
          job_post: jobPost,
        }),
      });

      const data = await response.json();

      // Adjust to handle API structure
      const aiFeedback =
        data?.choices?.[0]?.message?.content ||
        data?.feedback ||
        "No feedback received.";

      setFeedback(aiFeedback);
    } catch (error) {
      console.error(error);
      setFeedback("Error submitting resume. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Render Login if not logged in 
  if (!isLoggedIn) {
    return (
      <div className="App">
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
         
          <div style={{ marginBottom: "10px" }}>
            <label>Username:</label>
            <input
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div style={{ marginBottom: "10px" }}>
            <label>Password:</label>
            <input
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit">Login</button>
        </form>
      </div>
    );
  }

// Main App
  return (
    <div className="App">
      <h1>AI Resume Feedback</h1>
      <button onClick={handleLogout} style={{ float: "right" }}>
        Logout
      </button>

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "12px",
          marginBottom: "20px",
          marginTop: "40px",
        }}
      >
        <button onClick={() => setView("manual")} disabled={view === "manual"}>
          Manual Feedback
        </button>
        <button onClick={() => setView("jobs")} disabled={view === "jobs"}>
          View Saved Applications
        </button>
      </div>

      {view === "manual" && (
        <>
          <form onSubmit={handleSubmit}>
            <textarea
              rows="10"
              cols="80"
              placeholder="Paste your resume text here..."
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              required
            ></textarea>
            <br />
            <textarea
              rows="5"
              cols="80"
              placeholder="Paste job description or position here..."
              value={jobPost}
              onChange={(e) => setJobPost(e.target.value)}
            ></textarea>
            <br />
            <button type="submit" disabled={loading}>
              {loading ? "Analyzing..." : "Get Feedback"}
            </button>
          </form>

          {feedback && (
            <div style={{ marginTop: "20px", whiteSpace: "pre-wrap" }}>
              <h2>AI Feedback</h2>
              <ReactMarkdown>{feedback}</ReactMarkdown>
            </div>
          )}
        </>
      )}

      {view === "jobs" && (
        <div>
          {jobs.length === 0 ? (
            <p>Loading job applications...</p>
          ) : (
            jobs.map((job) => (
              <div
                key={job.id}
                style={{
                  border: "1px solid #ccc",
                  marginBottom: "15px",
                  padding: "15px",
                }}
              >
                <h3>
                  {job.position} @ {job.company_name}
                </h3>
                <p>Status: {job.status}</p>

                {job.application_date && (
                  <p>
                    <strong>Applied on:</strong> {job.application_date}
                  </p>
                )}

                {job.feedback && (
                  <div
                    style={{
                      background: "#f9f9f9",
                      padding: "10px",
                      marginTop: "10px",
                    }}
                  >
                    <h4>Resume Feedback</h4>
                    <ReactMarkdown>{job.feedback}</ReactMarkdown>
                  </div>
                )}

                {job.resume && (
                  <p>
                    <strong>Resume:</strong>{" "}
                    <a
                      href={job.resume}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Download
                    </a>
                  </p>
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default App;
