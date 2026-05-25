import { useState } from "react";

function PipelineInput({ onSend }) {
  const [input, setInput] = useState("");

  const handleSubmit = () => {
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  };

  return (
    <div style={styles.container}>
      <textarea
        rows={2}
        placeholder="Type your message here..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={styles.textarea}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
          }
        }}
      />
      <button onClick={handleSubmit} style={styles.sendButton}>
        Send
      </button>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    gap: "12px",
    width: "100%",
    alignItems: "flex-end",
  },

  textarea: {
    flex: 1,
    minHeight: "64px",
    maxHeight: "140px",
    padding: "14px 16px",
    borderRadius: "14px",
    border: "1px solid #3f3f46",
    backgroundColor: "#27272a",
    color: "#f4f4f5",
    fontSize: "15px",
    fontFamily: "inherit",
    resize: "vertical",
    outline: "none",
    boxShadow: "0 2px 6px rgba(0,0,0,0.25)",
  },

  sendButton: {
    padding: "0 22px",
    height: "48px",
    borderRadius: "12px",
    border: "1px solid #3f3f46",
    backgroundColor: "#3f3f46",
    color: "#f4f4f5",
    cursor: "pointer",
    fontWeight: 500,
    fontSize: "14px",
    transition: "all 0.2s ease",
  },
};

export default PipelineInput;





