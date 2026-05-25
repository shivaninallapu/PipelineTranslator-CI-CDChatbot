function ChatWindow({ history }) {
  return (
    <div style={{ padding: "10px", height: "60%", overflowY: "auto" }}>
      {history.map((msg, index) => (
        <div key={index}>
          <strong>{msg.role}:</strong>
          <p>{msg.content}</p>
        </div>
      ))}
    </div>
  );
}

export default ChatWindow;
