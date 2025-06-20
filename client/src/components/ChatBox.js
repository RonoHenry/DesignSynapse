import React, { useState, useRef, useEffect } from "react";
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/v1/ai/clientsync";

const ChatBox = () => {
  const [messages, setMessages] = useState([
    { sender: "AI", text: "Hey! What’s your project about? Budget, style, anything you wanna share?" }
  ]);
  const [input, setInput] = useState("");
  const [designBrief, setDesignBrief] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, designBrief]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    setErrorMsg("");
    setLoading(true);

    const newMessages = [...messages, { sender: "User", text: input }];
    setMessages(newMessages);
    setInput("");

    try {
      const response = await axios.post(API_URL, {
        messages: newMessages,
      });
      const brief = response.data.design_brief;
      setMessages([...newMessages, { sender: "AI", text: "Got it! Here’s your design brief:" }]);
      setDesignBrief(brief);
    } catch (error) {
      setMessages([...newMessages, { sender: "AI", text: "Oops, something went wrong!" }]);
      setErrorMsg("Failed to reach the server. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleInputKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4 bg-white rounded shadow">
      <div className="h-96 overflow-y-auto border p-4 mb-4 rounded bg-gray-50">
        {messages.map((msg, index) => (
          <div key={index} className={`mb-2 flex ${msg.sender === "User" ? "justify-end" : "justify-start"}`}>
            <span
              className={`inline-block p-2 rounded-lg max-w-xs break-words ${
                msg.sender === "User" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-900"
              }`}
              aria-label={msg.sender === "User" ? "Your message" : "AI message"}
            >
              {msg.text}
            </span>
          </div>
        ))}
        {designBrief && (
          <div className="mt-4 p-4 bg-green-100 rounded">
            <h3 className="font-bold mb-1">Design Brief:</h3>
            <p className="whitespace-pre-line">{designBrief}</p>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>
      {errorMsg && <div className="text-red-600 mb-2">{errorMsg}</div>}
      <form
        className="flex"
        onSubmit={e => {
          e.preventDefault();
          handleSend();
        }}
        aria-label="Chat input form"
      >
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleInputKeyDown}
          className="flex-1 p-2 border rounded-l focus:outline-none focus:ring"
          placeholder="Type your response..."
          aria-label="Type your response"
          disabled={loading}
          autoFocus
        />
        <button
          type="submit"
          className={`p-2 px-4 bg-blue-600 text-white rounded-r transition-opacity ${loading ? "opacity-50 cursor-not-allowed" : ""}`}
          disabled={loading}
          aria-label="Send message"
        >
          {loading ? "Sending..." : "Send"}
        </button>
      </form>
    </div>
  );
};

export default ChatBox;