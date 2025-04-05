import React, { useState } from "react";
import axios from "axios";

const ChatBox = () => {
  const [messages, setMessages] = useState([
    { sender: "AI", text: "Hey! What’s your project about? Budget, style, anything you wanna share?" }
  ]);
  const [input, setInput] = useState("");
  const [designBrief, setDesignBrief] = useState(null);

  const handleSend = async () => {
    if (!input.trim()) return;

    // Add user message to chat
    const newMessages = [...messages, { sender: "User", text: input }];
    setMessages(newMessages);
    setInput("");

    try {
      // Send input to backend API
      const response = await axios.post("http://localhost:8000/v1/ai/clientsync", {
        messages: newMessages,
      });
      const brief = response.data.design_brief;

      // Add AI response and brief
      setMessages([...newMessages, { sender: "AI", text: "Got it! Here’s your design brief:" }]);
      setDesignBrief(brief);
    } catch (error) {
      console.error("Error calling API:", error);
      setMessages([...newMessages, { sender: "AI", text: "Oops, something went wrong!" }]);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="h-96 overflow-y-auto border p-4 mb-4 rounded">
        {messages.map((msg, index) => (
          <div key={index} className={`mb-2 ${msg.sender === "User" ? "text-right" : "text-left"}`}>
            <span className={`inline-block p-2 rounded ${msg.sender === "User" ? "bg-blue-200" : "bg-gray-200"}`}>
              {msg.text}
            </span>
          </div>
        ))}
        {designBrief && (
          <div className="mt-4 p-4 bg-green-100 rounded">
            <h3 className="font-bold">Design Brief:</h3>
            <p>{designBrief}</p>
          </div>
        )}
      </div>
      <div className="flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleSend()}
          className="flex-1 p-2 border rounded-l"
          placeholder="Type your response..."
        />
        <button onClick={handleSend} className="p-2 bg-blue-500 text-white rounded-r">
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatBox;