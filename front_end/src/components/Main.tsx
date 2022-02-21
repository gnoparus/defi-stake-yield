import { useEthers } from "@usedapp/core"
import helperConfig from "../helper-config.json"
import networkMapping from "../chain-info/deployments/map.json"
import { constants } from "ethers";
import brownieConfig from "../brownie-config.json"

export const Main = () => {

    var { chainId, error } = useEthers();

    // const networkName = chainId ? helperConfig[chainId] : "dev"
    const networkName: string = chainId ? JSON.parse(JSON.stringify(helperConfig))[chainId] : "dev";

    console.log("chainId = ", chainId)
    console.log("networkName = ", networkName)

    const dappTokenAddress = chainId ? JSON.parse(JSON.stringify(networkMapping))[chainId]["DappToken"][0] : constants.AddressZero
    console.log("dappTokenAddress = ", dappTokenAddress)

    const wethTokenAddress = chainId ? JSON.parse(JSON.stringify(brownieConfig))["networks"][networkName]["weth_token"] : constants.AddressZero
    console.log("wethTokenAddress = ", wethTokenAddress)

    const fauTokenAddress = chainId ? JSON.parse(JSON.stringify(brownieConfig))["networks"][networkName]["fau_token"] : constants.AddressZero
    console.log("fauTokenAddress = ", fauTokenAddress)

    return (<div>Hi from Main!</div>)
}