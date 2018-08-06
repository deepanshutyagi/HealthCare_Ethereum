var Migrations = artifacts.require("./Migrations.sol");
var pricedirectory=artifacts.require("./PriceDirectory.sol");
module.exports = function(deployer) {
  deployer.deploy(Migrations);
  deployer.deploy(pricedirectory);
};
