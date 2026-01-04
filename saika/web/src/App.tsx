import { Collapsible, Menu } from "@base-ui-components/react"
import { Icon } from "@iconify/react"
import * as AP from "archipelago.js"
import { Activity, type ComponentProps, type ReactNode, useState } from "react"
import { useFormStatus } from "react-dom"
import { twMerge } from "tailwind-merge"

export function App() {
	type Server = {
		id: string
		name: string
		serverAddress: string
		serverPassword: string
		games: ServerGame[]
	}

	type Session = {
		id: string
		serverId: string
		gameName: string
		playerName: string
	}

	const [servers, setServers] = useState<Server[]>([
		{
			name: "friendsync",
			serverAddress: "archipelago.gg:40421",
			serverPassword: "",
			id: "908464b5-93f6-4583-b05e-b5a2c0e43ac1",
			games: [
				{
					id: "ChecksFinder",
					displayName: "ChecksFinder",
				},
				{
					id: "Minecraft",
					displayName: "Minecraft",
				},
				{
					id: "Portal 2",
					displayName: "Portal 2",
				},
				{
					id: "Sonic Riders",
					displayName: "Sonic Riders",
				},
				{
					id: "Starcraft 2",
					displayName: "Starcraft 2",
				},
			],
		},
	])

	const [sessions, setSessions] = useState<Session[]>([
		{
			gameName: "Minecraft",
			playerName: "MapleCraft",
			id: "d2fb52dc-7156-400c-8c53-5b2bec61d9d8",
			serverId: "908464b5-93f6-4583-b05e-b5a2c0e43ac1",
		},
		{
			gameName: "Portal 2",
			playerName: "MapleScience",
			id: "08757725-94ad-45bc-b022-5a00efa6dfc8",
			serverId: "908464b5-93f6-4583-b05e-b5a2c0e43ac1",
		},
	])

	console.log(servers, sessions)

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
			<ConnectView
				onSubmitServer={async (input) => {
					const client = new AP.Client()
					const roomInfo = await client.socket.connect(input.serverAddress)

					const id = crypto.randomUUID()

					const games = roomInfo.games
						.filter((id) => id !== "Archipelago")
						.map((id): ServerGame => ({ id, displayName: id }))
						.sort((a, b) =>
							a.displayName
								.toLocaleLowerCase()
								.localeCompare(b.displayName.toLocaleLowerCase()),
						)

					setServers((servers) => [
						...servers,
						{
							...input,
							id,
							games: games,
						},
					])
					setCurrentViewId(id)
				}}
			/>
		),
	}

	const settingsView: View = {
		id: "Settings",
		icon: "mingcute:settings-2-fill",
		content: <p>Settings</p>,
	}

	const serverViews = servers.map((server) => {
		const view = {
			id: server.id,
			label: server.name,
			icon: "mingcute:earth-3-fill",
			server,
			content: (
				<ServerView
					games={server.games}
					onSubmitSession={(input) => {
						const id = crypto.randomUUID()
						setSessions((sessions) => [
							...sessions,
							{
								...input,
								id,
								serverId: server.id,
							},
						])
					}}
				/>
			),
			sessionViews: sessions
				.filter((session) => session.serverId === server.id)
				.map(
					(session): View => ({
						id: session.id,
						label: session.playerName,
						sublabel: session.gameName,
						icon: "mingcute:game-2-fill",
						content: <SessionView {...server} {...session} />,
					}),
				),
		}
		return view satisfies View
	})

	const allViews: [View, ...View[]] = [
		connectView,
		...serverViews,
		...serverViews.flatMap((server) => server.sessionViews),
		settingsView,
	]

	const [currentViewId, setCurrentViewId] = useState(allViews[0].id)

	const currentView =
		allViews.find((view) => view.id === currentViewId) ?? allViews[0]

	const navItemProps = (view: View) => ({
		icon: view.icon,
		label: view.label || view.id,
		sublabel: view.sublabel,
		isCurrent: view.id === currentView.id,
		onClick: () => setCurrentViewId(view.id),
	})

	return (
		<div className="flex h-dvh w-dvw items-stretch gap-1.5">
			<div className="flex min-h-0 w-56 shrink-0 flex-col gap-1.5 bg-gray-900 p-2">
				<NavButton {...navItemProps(connectView)} />

				<div className="basis-px self-stretch bg-gray-700/70" />

				<div className="flex min-h-0 flex-1 flex-col gap-1.5 overflow-y-auto *:shrink-0">
					{serverViews.map((view) => (
						<NavCollapse
							key={view.id}
							{...navItemProps(view)}
							menuOptions={[
								{
									label: "Copy Address",
									icon: "mingcute:clipboard-fill",
									onClick: () => {
										navigator.clipboard.writeText(view.server.serverAddress)
									},
								},
								{
									label: "Rename",
									icon: "mingcute:edit-2-fill",
									onClick: () => {
										const newName = prompt(
											"Enter a new server name:",
											view.server.name,
										)

										if (newName === null) return

										setServers((servers) =>
											servers.map((s) =>
												s.id === view.server.id ? { ...s, name: newName } : s,
											),
										)
									},
								},
								{
									label: "Delete",
									icon: "mingcute:close-fill",
									onClick: () => {
										setServers((servers) =>
											servers.filter((s) => s.id !== view.server.id),
										)
									},
								},
							]}
						>
							{view.sessionViews.map((view) => (
								<NavButton
									key={view.id}
									{...navItemProps(view)}
									onClose={() => {
										setSessions((sessions) =>
											sessions.filter((s) => s.id !== view.id),
										)
									}}
								/>
							))}
						</NavCollapse>
					))}
				</div>

				<div className="basis-px self-stretch bg-gray-700/70" />

				<NavButton {...navItemProps(settingsView)} />
			</div>

			<div className="flex-1">
				{allViews.map((view) => (
					<Activity
						key={view.id}
						mode={view.id === currentViewId ? "visible" : "hidden"}
					>
						{view.content}
					</Activity>
				))}
			</div>
		</div>
	)
}

interface NavButtonProps extends React.ComponentProps<"button"> {
	icon: string
	label: ReactNode
	sublabel?: ReactNode
	isCurrent: boolean
	onClose?: () => void
}

function NavButton({
	icon,
	label,
	sublabel,
	isCurrent,
	className,
	onClick,
	onClose,
	...props
}: NavButtonProps) {
	return (
		<div
			className="flex w-full items-center rounded opacity-75 transition hover:bg-gray-800 hover:opacity-100 data-current:bg-gray-800 data-current:opacity-100"
			data-current={isCurrent || undefined}
		>
			<button
				type="button"
				onClick={onClick}
				className={twMerge(
					"flex min-h-10 flex-1 items-center justify-start gap-2 rounded px-3 py-2 -outline-offset-2 transition",
					className,
				)}
				{...props}
			>
				<Icon icon={icon} className="-mx-0.5 size-5 shrink-0" />
				<div className="flex min-w-0 flex-1 flex-col text-start">
					<span className="truncate text-base/tight">{label}</span>
					<span className="truncate text-gray-300/90 text-xs/tight">
						{sublabel}
					</span>
				</div>
			</button>

			<button
				type="button"
				data-visible={isCurrent && onClose ? true : undefined}
				className="flex size-8 items-center justify-center rounded opacity-0 -outline-offset-2 transition data-visible:opacity-100"
				onClick={(event) => {
					if (isCurrent) {
						onClose?.()
					} else {
						onClick?.(event)
					}
				}}
			>
				<Icon icon="mingcute:close-fill" className="-mx-0.5 size-5 shrink-0" />
				<span className="sr-only">Close</span>
			</button>
		</div>
	)
}

interface NavCollapseProps {
	label: ReactNode
	className?: string
	isCurrent: boolean
	onClick: () => void
	children: React.ReactNode
	menuOptions: {
		id?: string
		label: string
		icon: string
		onClick: () => void
	}[]
}

function NavCollapse(props: NavCollapseProps) {
	return (
		<Collapsible.Root className="contents" defaultOpen>
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
							<Menu.Popup className="flex min-w-40 origin-(--transform-origin) flex-col gap-1 rounded-md bg-gray-900 p-1 transition duration-100 data-starting-style:scale-95 data-ending-style:opacity-0 data-starting-style:opacity-0">
								{props.menuOptions.map((opt) => (
									<Menu.Item
										key={opt.id || opt.label}
										className="flex h-10 items-center justify-start gap-2 rounded px-3 transition hover:bg-gray-800"
										onClick={opt.onClick}
									>
										<Icon icon={opt.icon} className="-mx-0.5 size-5" />
										<span className="flex-1">{opt.label}</span>
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

function ConnectView({
	onSubmitServer,
}: {
	onSubmitServer: (values: {
		name: string
		serverAddress: string
		serverPassword: string
	}) => unknown
}) {
	return (
		<div className="grid size-full place-content-center gap-3">
			<h2 className="text-center font-light text-2xl text-gray-400">Connect</h2>
			<form
				className="flex w-80 flex-col gap-3 rounded-md bg-gray-800 p-3"
				method="post"
				action={async (formData) => {
					const name = formData.get("name") as string
					const serverAddress = formData.get("address") as string
					const serverPassword = (formData.get("password") || "") as string
					if (!serverAddress) return

					try {
						await onSubmitServer({
							name: name || serverAddress,
							serverAddress,
							serverPassword,
						})
					} catch (error) {
						console.error(error)
						alert(
							`Error: ${
								(error as Error)?.message ?? "An unknown error occurred"
							}`,
						)
					}
				}}
			>
				<label>
					<div className="text-gray-300 text-sm">Server Name</div>
					<input
						name="name"
						className="h-10 w-full min-w-0 rounded bg-black/40 px-3 focus:bg-black/70"
						placeholder="The Best Multi Ever"
					/>
				</label>
				<label>
					<div className="text-gray-300 text-sm">Server Address</div>
					<input
						name="address"
						required
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
				<FormButton icon="mingcute:plugin-fill">Connect</FormButton>
			</form>
		</div>
	)
}

type ServerGame = {
	id: string
	displayName: string
}

function ServerView({
	games,
	onSubmitSession,
}: {
	games: ServerGame[]
	onSubmitSession: (values: { gameName: string; playerName: string }) => unknown
}) {
	return (
		<div className="grid size-full place-content-center gap-3">
			<h2 className="text-center font-light text-2xl text-gray-400">
				Enter Player Details
			</h2>
			<form
				className="flex w-80 flex-col gap-3 rounded-md bg-gray-800 p-3"
				action={async (formData) => {
					const gameName = formData.get("game") as string
					const playerName = formData.get("player") as string
					if (!playerName) return

					try {
						await onSubmitSession({
							gameName,
							playerName,
						})
					} catch (error) {
						console.error(error)
						alert(
							`Error: ${
								(error as Error)?.message ?? "An unknown error occurred"
							}`,
						)
					}
				}}
			>
				<label>
					<div className="text-gray-300 text-sm">Game</div>
					<select
						name="game"
						className="h-10 w-full min-w-0 rounded bg-black/40 px-3 focus:bg-black/70"
					>
						{games.map((game) => (
							<option key={game.id} value={game.id}>
								{game.displayName}
							</option>
						))}
					</select>
				</label>

				<label>
					<div className="text-gray-300 text-sm">Player Name</div>
					<input
						name="player"
						className="h-10 w-full min-w-0 rounded bg-black/40 px-3 focus:bg-black/70"
						placeholder="HatKid"
					/>
				</label>

				<FormButton icon="mingcute:open-door-fill">Enter</FormButton>
			</form>
		</div>
	)
}

function FormButton({
	children,
	icon,
	...props
}: ComponentProps<"button"> & { icon: string }) {
	const status = useFormStatus()
	console.log(status)
	return (
		<button
			type="submit"
			disabled={status.pending}
			{...props}
			className={twMerge(
				"flex h-10 items-center justify-center gap-2 rounded bg-black/40 px-3 hover:bg-black/60 active:bg-black/90 active:duration-0 disabled:opacity-50",
				props.className,
			)}
		>
			<span className="-mx-0.5 *:size-5">
				{status.pending ? (
					<Icon icon="mingcute:loading-3-fill" className="animate-spin" />
				) : (
					<Icon icon={icon} />
				)}
			</span>
			<span>{children}</span>
		</button>
	)
}

function SessionView(props: {
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
