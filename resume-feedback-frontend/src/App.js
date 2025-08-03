import React, {useState} from "react"; //{ useState } is a React Hook that lets us add state (variables) to our functional component
import "./App.css";
function App(){
  const [resumeText, setResumeText]=useState("");
  const [feedback, setFeedback]=useState("");
  const [loading, setLoading]=useState(false);

  const handleSubmit=async(e)=>{
    e.preventDefault(); //e.preventDefault() stops the browser from refreshing the page on submit
    setLoading(true);
    setFeedback("");

    try{
      const response=await fetch("http://127.0.0.1:8000/api/get-resume-feedback/",{
        method: "POST",
        headers:{
          "Content-Type": "application/json",
        },
        body: JSON.stringify({resume_text: resumeText}),
      });

      const data=await response.json();
      setFeedback(data.feedback || "No feedback recieved");
    }
    catch (error){
      setFeedback("Error submitting resume. Please try again");
    }
    finally{
      setLoading(false);
    }
  };

  return(
    <div className="App">
      <h1>Resume Feedback AI</h1>
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
        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Get Feedback"}
        </button>
      </form>

      {feedback && (
        <div style={{ marginTop: "20px", whiteSpace: "pre-wrap" }}>
          <h2>AI Feedback</h2>
          <p>{feedback}</p>
        </div>
  )}
 </div>
  );
}

export default App;

