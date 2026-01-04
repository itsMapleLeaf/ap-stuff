import { Collapsible, Menu } from "@base-ui-components/react"
import { Icon } from "@iconify/react"
import { type ReactNode, useState } from "react"
import { twMerge } from "tailwind-merge"

export function App() {
	type Servers = {
		id: string
		serverAddress: string
		serverPassword: string
		sessions: {
			id: string
			gameName: string
			playerName: string
		}[]
	}

	const [servers, setServers] = useState<Servers[]>([])

	type View = {
		id: string
		label?: ReactNode
		sublabel?: ReactNode
		icon: string
		content: ReactNode
	}

	const connectView: View = {
		id: "Connect",
		icon: "mingcute:plugin-fill",
		content: (
			<Connect
				onSubmit={({ serverAddress, serverPassword }) => {
					setServers((servers) => [
						...servers,
						{
							id: crypto.randomUUID(),
							serverAddress,
							serverPassword,
							sessions: [],
						},
					])
				}}
			/>
		),
	}

	const settingsView: View = {
		id: "Settings",
		icon: "mingcute:settings-2-fill",
		content: <p>Settings</p>,
	}

	const serverViews = servers.map(
		(server): View => ({
			id: server.id,
			label: server.serverAddress,
			icon: "mingcute:earth-3-fill",
			content: <p>server {server.serverAddress}</p>,
		}),
	)

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
		// ...sessionViews,
		...serverViews,
		settingsView,
	]

	const [currentView, setCurrentView] = useState(allViews[0])

	const navItemProps = (view: View) => ({
		icon: view.icon,
		label: view.label || view.id,
		sublabel: view.sublabel,
		isCurrent: view.id === currentView.id,
		onClick: () => setCurrentView(view),
	})

	return (
		<div className="flex h-dvh w-dvw items-stretch gap-1.5">
			<div className="flex min-h-0 w-56 shrink-0 flex-col gap-1.5 bg-gray-900 p-2">
				<NavButton {...navItemProps(connectView)} />

				<div className="basis-px self-stretch bg-gray-700/70" />

				<div className="flex min-h-0 flex-1 flex-col gap-1.5 overflow-y-auto *:shrink-0">
					{serverViews.map((view) => (
						<NavCollapse key={view.id} {...navItemProps(view)}>
							{sessionViews.map((view) => (
								<NavButton key={view.id} {...navItemProps(view)} />
							))}
						</NavCollapse>
					))}
				</div>

				<div className="basis-px self-stretch bg-gray-700/70" />

				<NavButton {...navItemProps(settingsView)} />
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

interface NavCollapseProps {
	label: ReactNode
	className?: string
	isCurrent: boolean
	onClick: () => void
	children: React.ReactNode
}

function NavCollapse(props: NavCollapseProps) {
	return (
		<Collapsible.Root className="contents">
			<div
				className="group flex min-h-7 w-full rounded opacity-75 transition duration-150 hover:bg-gray-800 hover:opacity-100 data-current:bg-gray-800 data-current:opacity-100"
				data-current={props.isCurrent || undefined}
			>
				<Collapsible.Trigger
					render={<div />}
					className={twMerge(
						"flex aspect-square h-full shrink-0 items-center justify-center rounded transition hover:bg-gray-800",
						"group",
						props.className,
					)}
				>
					<Icon
						icon="mingcute:right-fill"
						className="size-4 shrink-0 group-data-panel-open:rotate-90"
					/>
				</Collapsible.Trigger>

				<button
					type="button"
					className="w-full flex-1 truncate rounded text-start text-gray-300 text-sm opacity-75 -outline-offset-2 transition duration-150 hover:bg-gray-800 hover:opacity-100 data-current:bg-gray-800 data-current:opacity-100"
					data-current={props.isCurrent || undefined}
					onClick={props.onClick}
				>
					{props.label}
				</button>

				<Menu.Root>
					<Menu.Trigger className="flex aspect-square h-full shrink-0 items-center justify-center rounded opacity-0 transition hover:bg-gray-800 group-focus-within:opacity-100 group-hover:opacity-100">
						<Icon icon="mingcute:more-2-fill" className="size-4 shrink-0" />
					</Menu.Trigger>
					<Menu.Portal>
						<Menu.Positioner side="right" sideOffset={12} align="start">
							<Menu.Popup className="flex min-w-40 origin-(--transform-origin) flex-col gap-1 rounded-md bg-gray-800 p-1 transition duration-100 data-starting-style:scale-95 data-ending-style:opacity-0 data-starting-style:opacity-0">
								{["one", "two", "three"].map((text) => (
									<Menu.Item
										key={text}
										className="flex h-10 items-center justify-start gap-2 rounded bg-black/40 px-3 hover:bg-black/60 active:bg-black/90 active:duration-0"
									>
										<Icon
											icon="mingcute:plugin-fill"
											className="-mx-0.5 size-5"
										/>
										<span className="flex-1">{text}</span>
									</Menu.Item>
								))}
							</Menu.Popup>
						</Menu.Positioner>
					</Menu.Portal>
				</Menu.Root>
			</div>
			<Collapsible.Panel className="contents">
				{props.children}
			</Collapsible.Panel>
		</Collapsible.Root>
	)
}

function Connect({
	onSubmit,
}: {
	onSubmit: (values: {
		serverAddress: string
		serverPassword: string
	}) => unknown
}) {
	return (
		<div className="grid size-full place-content-center gap-3">
			<h2 className="text-center font-light text-2xl text-gray-400">Connect</h2>
			<form
				className="flex w-80 flex-col gap-3 rounded-md bg-gray-800 p-3"
				action={async (formData) => {
					await onSubmit({
						serverAddress: formData.get("address") as string,
						serverPassword: formData.get("pasword") as string,
					})
				}}
			>
				<label>
					<div className="text-gray-300 text-sm">Server Address</div>
					<input
						name="address"
						className="h-10 w-full min-w-0 rounded bg-black/40 px-3 focus:bg-black/70"
						placeholder="archipelago.gg:69420"
					/>
				</label>
				<label>
					<div className="text-gray-300 text-sm">Password</div>
					<input
						name="password"
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
