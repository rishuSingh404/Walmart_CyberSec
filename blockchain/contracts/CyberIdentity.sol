// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CyberIdentity {
    struct Session { bytes32 hash; uint256 timestamp; }

    mapping(address => bool) public registered;
    mapping(address => string) public didDoc;
    mapping(address => Session[]) public sessions;

    event DIDRegistered(address indexed user, string didDocument);
    event SessionLogged(address indexed user, bytes32 sessionHash, uint256 timestamp);

    function registerDID(string memory didDocument) public {
        require(!registered[msg.sender], "DID already registered");
        registered[msg.sender] = true;
        didDoc[msg.sender] = didDocument;
        emit DIDRegistered(msg.sender, didDocument);
    }

    function verifyDID(address user) public view returns(bool) {
        return registered[user];
    }

    function logSession(bytes32 sessionHash) public {
        require(registered[msg.sender], "DID not registered");
        sessions[msg.sender].push(Session(sessionHash, block.timestamp));
        emit SessionLogged(msg.sender, sessionHash, block.timestamp);
    }

    function getSessionCount(address user) public view returns(uint256) {
        return sessions[user].length;
    }
}
