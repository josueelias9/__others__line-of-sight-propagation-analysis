import bcrypt from 'bcrypt'
import postgres from 'postgres'
import { id } from 'zod/v4/locales'

const sql = postgres(process.env.POSTGRES_URL!, {
    ssl: process.env.POSTGRES_SSL === 'require' ? 'require' : false
})

const users = [
    {
        id: 0,
        email: 'user@example.com',
        password: 'password123',
        is_active: true,
        is_superuser: false
    }
]

async function seedUsers() {
    const insertedUsers = await Promise.all(
        users.map(async user => {
            const hashedPassword = await bcrypt.hash(user.password, 10)
            return sql`
                INSERT INTO users (id, email, hashed_password, is_active, is_superuser)
                VALUES (${user.id}, ${user.email}, ${hashedPassword}, ${user.is_active}, ${user.is_superuser})
                ON CONFLICT (id) DO NOTHING
            `
        })
    )

    return insertedUsers
}

export async function GET() {
    try {
        await seedUsers()
        return Response.json({ message: 'Database seeded successfully' })
    } catch (error) {
        return Response.json({ error }, { status: 500 })
    }
}
