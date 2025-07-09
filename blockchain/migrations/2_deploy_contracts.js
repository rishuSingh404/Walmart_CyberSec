const CyberIdentity = artifacts.require("CyberIdentity");

module.exports = function (deployer) {
  deployer.deploy(CyberIdentity);
};
