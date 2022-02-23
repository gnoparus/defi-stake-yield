

interface BalanceMsgProps {
    label: string
    amount: number
    tokenImgSrc: string
}

export const BalanceMsg = ({ label, amount, tokenImgSrc }: BalanceMsgProps) => {

    return (<div>
        <div>{label}</div>
        <div>{amount}</div>
        <img src={tokenImgSrc} alt="Token Logo" />
    </div>)
}