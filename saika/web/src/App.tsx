export function App() {
	const viewMap = {
		Connect: {
			icon: "",
			content: <p>Connect</p>,
		},
		// Connect: {
		// 	icon: "",
		// 	content: <p>Connect</p>,
		// },
		Settings: {
			icon: "",
			content: <p>Settings</p>,
		},
	}

	const views = Object.entries(viewMap).map(([name, config]) => ({
		name,
		...config,
	}))

	return (
		<div className="flex h-dvh items-stretch gap-3 p-3">
			<div className="flex w-48 flex-col gap-3">
				{views.map((view) => (
					<button
						key={view.name}
						type="button"
						className="flex h-10 items-center justify-start rounded bg-gray-800 px-3"
					>
						{view.name}
					</button>
				))}
			</div>
			<div className="flex-1 rounded bg-gray-800">view</div>
		</div>
	)
}
