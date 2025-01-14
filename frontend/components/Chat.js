import { useState } from 'react';

const Chat = ({ results }) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSend = () => {
    if (input.trim() !== '') {
      setMessages([...messages, { type: 'user', text: input }]);
      setInput('');
      // Simulate API call and response
      setTimeout(() => {
        const response = results.join(', ');
        setMessages([...messages, { type: 'user', text: input }, { type: 'bot', text: response }]);
      }, 1000);
    }
  };

  return (
    <div>
      <div>
        {messages.map((message, index) => (
          <div key={index} className={message.type}>
            {message.text}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={handleInputChange}
        placeholder="Type your message..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
};

export default Chat;
