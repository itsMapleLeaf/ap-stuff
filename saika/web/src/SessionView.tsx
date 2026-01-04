export function SessionView(props: {
	serverAddress: string
	serverPassword: string
	gameName: string
	playerName: string
}) {
	return (
		<p>
			session for {props.playerName} playing {props.gameName}
		</p>
	)
}
