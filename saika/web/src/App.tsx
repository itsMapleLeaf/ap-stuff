import { Icon } from "@iconify/react"
import { type ReactNode, useState } from "react"
import { twMerge } from "tailwind-merge"

export function App() {
	type Session = {
		serverAddress: string
		serverPassword: string
		gameName: string
		playerName: string
	}

	const [sessions, setSessions] = useState<Session[]>([])

	type View = {
		id: string
		sublabel?: ReactNode
		icon: string
		content: ReactNode
	}

	const connectView: View = {
		id: "Connect",
		icon: "mingcute:plugin-fill",
		content: <Connect />,
	}

	const settingsView: View = {
		id: "Settings",
		icon: "mingcute:settings-2-fill",
		content: <p>Settings</p>,
	}

	const sessionViews = ["MapleVoltex", "MapleCraft", "MapleScience"].map(
		(name): View => ({
			id: name,
			sublabel: "address",
			icon: "mingcute:game-2-fill",
			content: <p>{name}</p>,
		}),
	)

	const allViews: [View, ...View[]] = [
		connectView,
		...sessionViews,
		settingsView,
	]

	const [currentView, setCurrentView] = useState(allViews[0])

	const navButtonProps = (view: View): NavButtonProps => ({
		icon: view.icon,
		label: view.id,
		sublabel: view.sublabel,
		isCurrent: view.id === currentView.id,
		onClick: () => setCurrentView(view),
	})

	return (
		<div className="flex h-dvh w-dvw items-stretch gap-1.5">
			<div className="flex min-h-0 w-52 shrink-0 flex-col gap-1.5 bg-gray-900 p-2">
				<NavButton {...navButtonProps(connectView)} />

				<div className="basis-px self-stretch bg-gray-700/70" />

				<div className="flex min-h-0 flex-1 flex-col gap-1.5 overflow-y-auto *:shrink-0">
					{sessionViews.map((view) => (
						<NavButton key={view.id} {...navButtonProps(view)} />
					))}
				</div>

				<div className="basis-px self-stretch bg-gray-700/70" />

				<NavButton {...navButtonProps(settingsView)} />
			</div>

			<div className="flex-1">{currentView.content}</div>
		</div>
	)
}

interface NavButtonProps extends React.ComponentProps<"button"> {
	icon: string
	label: ReactNode
	sublabel?: ReactNode
	isCurrent: boolean
}

function NavButton(props: NavButtonProps) {
	return (
		<button
			type="button"
			data-current={props.isCurrent || undefined}
			{...props}
			className={twMerge(
				"flex min-h-10 w-full items-center justify-start gap-2 rounded px-3 py-2 opacity-75 -outline-offset-2 transition duration-150 hover:bg-gray-800 hover:opacity-100 data-current:bg-gray-800 data-current:opacity-100",
				props.className,
			)}
		>
			<Icon icon={props.icon} className="-mx-0.5 size-5 shrink-0" />
			<div className="flex min-w-0 flex-1 flex-col text-start">
				<span className="truncate text-base/tight">{props.label}</span>
				<span className="truncate text-gray-300/90 text-xs/tight">
					{props.sublabel}
				</span>
			</div>
		</button>
	)
}

function Connect() {
	return (
		<div className="grid size-full place-content-center gap-3">
			<h2 className="text-center font-light text-2xl text-gray-400">Connect</h2>
			<form
				className="flex w-80 flex-col gap-3 rounded-md bg-gray-800 p-3"
				action={() => {}}
			>
				<label>
					<div className="text-gray-300 text-sm">Server Address</div>
					<input
						className="h-10 w-full min-w-0 rounded bg-black/40 px-3 focus:bg-black/70"
						placeholder="archipelago.gg:69420"
					/>
				</label>
				<label>
					<div className="text-gray-300 text-sm">Password</div>
					<input
						className="h-10 w-full min-w-0 rounded bg-black/40 px-3 focus:bg-black/70"
						placeholder="••••••••"
					/>
				</label>
				<button
					type="submit"
					className="flex h-10 items-center justify-center gap-2 rounded bg-black/40 px-3 hover:bg-black/60 active:bg-black/90 active:duration-0"
				>
					<Icon icon="mingcute:plugin-fill" className="-mx-0.5 size-5" />
					Connect
				</button>
			</form>
		</div>
	)
}
