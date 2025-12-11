import Link from "next/link";

export default function AdminHome() {
    return (
        <>
            <Link href={`admin/groups/create`}>グループ作成</Link>
            <Link href={`admin/groups`}>グループ一覧</Link>
            <Link href={`admin/users/create`}>ユーザー作成</Link>
            <Link href={`admin/users`}>ユーザー一覧</Link>
        </>
    )
}