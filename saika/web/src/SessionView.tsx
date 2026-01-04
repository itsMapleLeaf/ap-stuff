import { Tabs } from "@base-ui-components/react"
import type { ReactNode } from "react"

export function SessionView(props: {
	serverAddress: string
	serverPassword: string
	gameName: string
	playerName: string
}) {
	const views: { id: string; content: ReactNode }[] = [
		{ id: "Chat", content: <>Chat</> },
		{ id: "Items", content: <>Items</> },
		{ id: "Locations", content: <>Locations</> },
		{ id: "Hints", content: <>Hints</> },
		{ id: "Settings", content: <>Settings</> },
	]

	return (
		<Tabs.Root className="flex flex-col gap-2 p-2" defaultValue={views[0]?.id}>
			<Tabs.List className="flex gap-2">
				{views.map((view) => (
					<Tabs.Tab
						key={view.id}
						value={view.id}
						className="h-10 rounded px-3 opacity-75 transition hover:bg-gray-800 data-active:bg-gray-800 data-active:opacity-100"
					>
						{view.id}
					</Tabs.Tab>
				))}
			</Tabs.List>
			{views.map((view) => (
				<Tabs.Panel key={view.id} value={view.id}>
					{view.content}
				</Tabs.Panel>
			))}
		</Tabs.Root>
	)
}
