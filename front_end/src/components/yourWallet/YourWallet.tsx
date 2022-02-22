import { Token } from "../Main"
import React, { useState } from "react"
import { Box, Tab } from '@mui/material';
import TabList from '@mui/lab/TabList';
import TabContext from '@mui/lab/TabContext';
import { TabPanel } from "@mui/lab";
import { WalletBalance } from "./WalletBalance";

interface YourWalletProps {
    supportedTokens: Array<Token>
}
export const YourWallet = ({ supportedTokens }: YourWalletProps) => {
    const [selectedTokenIndex, setSelectedTokenIndex] = useState<number>(0)

    const handleChange = (event: React.ChangeEvent<{}>, newValue: string) => {
        setSelectedTokenIndex(parseInt(newValue))
    }

    return (<Box>
        <h1>Your Wallet!</h1>
        <Box>
            <TabContext value={selectedTokenIndex.toString()}>
                <TabList onChange={handleChange} aria-label="stake form tabs">
                    {supportedTokens.map((token, index) => {
                        return (
                            <Tab label={token.name} value={index.toString()} key={index} />
                        )
                    })
                    }
                </TabList>
                {supportedTokens.map((token, index) => {
                    return (
                        <TabPanel value={index.toString()} key={index}>
                            <div>
                                wallet balance
                                stake button
                                <WalletBalance token={supportedTokens[selectedTokenIndex]} />
                            </div>
                        </TabPanel>
                    )
                })}
            </TabContext>
        </Box>
    </Box>)
}