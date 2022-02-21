import { useEthers } from "@usedapp/core"
import helperConfig from "../helper-config.json"

export const Main = () => {

    var { chainId } = useEthers();
    // const networkName = chainId ? helperConfig[chainId] : "dev"
    const networkName: string = chainId ? JSON.parse(JSON.stringify(helperConfig))[chainId] : "dev";
    // const dappTokenAddress;

    return (<div>Hi from Main!</div>)
}