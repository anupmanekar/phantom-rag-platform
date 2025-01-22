"use client";
import { useState } from "react";
import { sendMessage } from "@/app/api/llm-apis";

export default function Chat() {
  const [messages, setMessages] = useState<{ text: string; sender: string }[]>([]);
  const [input, setInput] = useState("");

  const handleSendMessage = async () => {
    if (input.trim() === "") return;

    const newMessage = { text: input, sender: "user" };
    setMessages([...messages, newMessage]);

    const data = await sendMessage(input);
    const botMessage = { text: data.results, sender: "bot" };
    setMessages((prevMessages) => [...prevMessages, botMessage]);
    setInput("");
  };

  return (
    <div>
      <div className="messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.sender === "user" ? "user" : "bot"}`}
          >
            {message.text}
          </div>
        ))}
      </div>
      <div>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <div>
         <button onClick={handleSendMessage}>Send</button>
        </div>
        
      </div>
    </div>
  );
}
