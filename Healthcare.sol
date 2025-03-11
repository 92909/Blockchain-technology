// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HealthcareCommunication {
    enum UserType { Patient, Doctor, Provider }
    
    struct User {
        address userAddress;
        string name;
        UserType userType;
        bool registered;
    }
    
    struct Message {
        address sender;
        address receiver;
        string content;
        uint256 timestamp;
    }
    
    mapping(address => User) public users;
    mapping(address => Message[]) private messages;
    
    event UserRegistered(address indexed user, string name, UserType userType);
    event MessageSent(address indexed sender, address indexed receiver, string content, uint256 timestamp);
    
    modifier onlyRegistered() {
        require(users[msg.sender].registered, "User not registered");
        _;
    }
    
    function registerUser(string memory _name, UserType _userType) public {
        require(!users[msg.sender].registered, "User already registered");
        users[msg.sender] = User(msg.sender, _name, _userType, true);
        emit UserRegistered(msg.sender, _name, _userType);
    }
    
    function sendMessage(address _receiver, string memory _content) public onlyRegistered {
        require(users[_receiver].registered, "Receiver not registered");
        messages[_receiver].push(Message(msg.sender, _receiver, _content, block.timestamp));
        emit MessageSent(msg.sender, _receiver, _content, block.timestamp);
    }
    
    function getMessages() public view onlyRegistered returns (Message[] memory) {
        return messages[msg.sender];
    }
}
