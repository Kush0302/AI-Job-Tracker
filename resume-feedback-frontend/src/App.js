import React, { useState, useEffect } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";

function App() {
  const [view, setView] = useState("manual"); // manual or jobs

  // For manual resume feedback
  const [resumeText, setResumeText] = useState("");
  const [jobPost, setJobPost] = useState("");
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);

  // For job applications
  const [jobs, setJobs] = useState([]);

  // Fetch job data from Django
  useEffect(() => {
    if (view === "jobs") {
      fetch("http://127.0.0.1:8000/api/job-applications/")
        .then((res) => res.json())
        .then((data) => setJobs(data))
        .catch((err) => console.error("Error loading jobs:", err));
    }
  }, [view]);

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

      // ✅ Adjust to handle API structure
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

  return (
    <div className="App">
      <h1>AI Resume Feedback</h1>

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "12px",
          marginBottom: "20px",
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
