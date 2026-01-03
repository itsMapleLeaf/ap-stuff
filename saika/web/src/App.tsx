import { Icon } from "@iconify/react"
import { type JSX, useState } from "react"

export function App() {
	type View = {
		name: string
		icon: string
		content: JSX.Element
	}

	const views: [View, ...View[]] = [
		{
			name: "Connect",
			icon: "mingcute:plugin-fill",
			content: <p>Connect</p>,
		},
		{
			name: "Settings",
			icon: "mingcute:settings-2-fill",
			content: <p>Settings</p>,
		},
	]

	const [currentView, setCurrentView] = useState(views[0])

	return (
		<div className="flex h-dvh items-stretch gap-2 p-3">
			<div className="flex w-48 flex-col gap-2">
				{views.map((view) => (
					<button
						key={view.name}
						type="button"
						data-current={view.name === currentView.name || undefined}
						className="flex h-10 items-center justify-start gap-2 rounded px-3 opacity-75 transition duration-150 hover:bg-gray-800 hover:opacity-100 data-current:bg-gray-800 data-current:opacity-100"
						onClick={() => setCurrentView(view)}
					>
						<Icon icon={view.icon} className="-mx-0.5 size-5" />
						{view.name}
					</button>
				))}
			</div>
			<div className="flex-1 rounded bg-gray-800">{currentView.content}</div>
		</div>
	)
}
