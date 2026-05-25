import { useState, useEffect, useRef } from "react";
import PipelineInput from "./PipelineInput";
import { FaPaperPlane } from "react-icons/fa";

function PipelineTranslator() {
  const [history, setHistory] = useState([]);
  const [isThinking, setIsThinking] = useState(false);
  const [thinkingDots, setThinkingDots] = useState("");
  const chatEndRef = useRef(null);

  useEffect(() => {
    const welcome = {
      role: "assistant",
      content:
        "Hi there! I can help you translate pipeline configurations between technologies. Please tell me your source and target technologies, what information you need, and any additional details like your team or project context.",
    };
    setHistory([welcome]);
  }, []);

  useEffect(() => {
    if (!isThinking) {
      setThinkingDots("");
      return;
    }

    const intervalId = setInterval(() => {
      setThinkingDots((prev) => (prev.length >= 3 ? "" : `${prev}.`));
    }, 350);

    return () => clearInterval(intervalId);
  }, [isThinking]);

  const handleSend = async (message) => {
    if (!message.trim() || isThinking) return;

    const newHistory = [...history, { role: "user", content: message }];
    setHistory(newHistory);
    setIsThinking(true);

    try {
      const res = await fetch("/api/chat/text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          conversation_history: newHistory,
        }),
      });

      const data = await res.json();

      setHistory((prev) => [
        ...prev,
        { role: "assistant", content: data?.message || "..." },
      ]);
    } catch (err) {
      console.error(err);
    } finally {
      setIsThinking(false);
    }
  };

  // Auto-scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history]);

  return (
    <div style={styles.page}>
      {/* Header */}
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>Pipeline Translator</h1>
          <p style={styles.subtitle}>
            Convert pipeline configurations between technologies
          </p>
        </div>
      </div>

      {/* Chat Area */}
      <div style={styles.chatPanel}>
        {history.map((msg, idx) => (
          <div
            key={idx}
            style={{
              ...styles.messageRow,
              justifyContent:
                msg.role === "user" ? "flex-end" : "flex-start",
            }}
          >
            {msg.role === "assistant" && (
              <div style={styles.aiAvatar}>AI</div>
            )}

            <div
              style={{
                ...styles.messageBubble,
                backgroundColor:
                  msg.role === "user"
                    ? "#3f3f46" // user bubble
                    : "#27272a", // assistant bubble
              }}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {isThinking && (
          <div
            style={{
              ...styles.messageRow,
              justifyContent: "flex-start",
            }}
          >
            <div style={styles.aiAvatar}>AI</div>
            <div
              style={{
                ...styles.messageBubble,
                backgroundColor: "#27272a",
              }}
            >
              Thinking{thinkingDots}
            </div>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Input Bar */}
      <div style={styles.inputBar}>
        <PipelineInput
          onSend={handleSend}
          style={styles.inputBox}
          placeholder="Type your message here..."
          sendIcon={<FaPaperPlane style={styles.sendIcon} />}
        />
      </div>
    </div>
  );
}

const styles = {
  page: {
    display: "flex",
    flexDirection: "column",
    height: "100vh",
    background: "linear-gradient(135deg, #18181b, #27272a)",
    color: "#f4f4f5",
    fontFamily: "'Inter', 'Segoe UI', sans-serif",
  },

  header: {
    padding: "22px 32px",
    borderBottom: "1px solid #2f2f35",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#18181b",
  },

  title: {
    margin: 0,
    fontSize: "26px",
    fontWeight: 600,
    letterSpacing: "-0.5px",
  },

  subtitle: {
    margin: "6px 0 0",
    color: "#a1a1aa",
    fontSize: "16px",
  },

  chatPanel: {
    flex: 1,
    padding: "28px",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: "14px",
  },

  messageRow: {
    display: "flex",
    alignItems: "flex-start",
    gap: "10px",
  },

  messageBubble: {
    padding: "14px 18px",
    borderRadius: "18px",
    maxWidth: "70%",
    wordBreak: "break-word",
    fontSize: "15px",
    lineHeight: "1.5",
    boxShadow: "0 4px 12px rgba(0,0,0,0.25)",
  },

  aiAvatar: {
    width: "36px",
    height: "36px",
    borderRadius: "50%",
    backgroundColor: "#3f3f46",
    color: "#e4e4e7",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: 600,
    fontSize: "13px",
  },

  inputBar: {
    padding: "20px 32px",
    borderTop: "1px solid #2f2f35",
    backgroundColor: "#18181b",
    display: "flex",
    gap: "12px",
  },

  inputBox: {
    flex: 1,
    minHeight: "70px",
    maxHeight: "160px",
    padding: "14px",
    borderRadius: "14px",
    border: "1px solid #3f3f46",
    backgroundColor: "#27272a",
    color: "#f4f4f5",
    fontSize: "15px",
    resize: "vertical",
  },

  sendIcon: {
    fontSize: "22px",
    cursor: "pointer",
    color: "#a1a1aa",
  },
};

export default PipelineTranslator;






