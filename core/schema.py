import sqlite3
import discord


class SchemaHandler:
    def __init__(self, database, client):
        self.database = database
        self.client = client
        self.version = self.version_check()

    def version_check(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("SELECT version FROM dbinfo;")
        version = cursor.fetchall()
        cursor.close()
        conn.close()
        if not version:
            self.set_version(0)
            return 0

        version = version[0][0]
        return version

    def set_version(self, version):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        if version > 0:
            previous = version - 1
            cursor.execute(
                "UPDATE dbinfo SET version = ? WHERE version = ?;", (version, previous)
            )

        else:
            cursor.execute("INSERT INTO dbinfo(version) values(?);", (version,))

        conn.commit()
        cursor.close()
        conn.close()
        self.version = version

    def zero_to_one(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(messages);")
        result = cursor.fetchall()
        columns = [value[1] for value in result]
        if "guild_id" not in columns:
            cursor.execute("ALTER TABLE messages ADD COLUMN 'guild_id' INT;")
            conn.commit()

        cursor.close()
        conn.close()
        self.set_version(1)

    def one_to_two(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(admins);")
        result = cursor.fetchall()
        columns = [value[1] for value in result]
        if "guild_id" not in columns:
            cursor.execute("SELECT role_id FROM admins")
            admins = cursor.fetchall()
            admins2 = [admin[0] for admin in admins]
            admins = admins2
            guilds = {}
            for guild in self.client.guilds:
                guilds[guild.id] = []
                for admin_id in admins:
                    role = discord.utils.get(guild.roles, id=admin_id)
                    if role is not None:
                        guilds[guild.id].append(role.id)

            cursor.execute("ALTER TABLE admins ADD COLUMN 'guild_id' INT;")
            conn.commit()
            for guild, value in guilds.items():
                for admin_id in value:
                    cursor.execute(
                        "UPDATE admins SET guild_id = ? WHERE role_id = ?;",
                        (guild, admin_id),
                    )
            cursor.execute("DELETE FROM admins WHERE guild_id IS NULL;")
            conn.commit()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='systemchannels';"
        )
        systemchannels_table = cursor.fetchall()
        if systemchannels_table:
            cursor.execute("SELECT * FROM systemchannels;")
            entries = cursor.fetchall()
            notify = 0  # Set default to not notify
            for entry in entries:
                guild_id = entry[0]
                channel_id = entry[1]
                cursor.execute(
                    "INSERT INTO guild_settings ('guild_id', 'notify', 'systemchannel') values(?, ?, ?);",
                    (guild_id, notify, channel_id),
                )
            cursor.execute("DROP TABLE systemchannels;")
            conn.commit()

        cursor.close()
        conn.close()
        self.set_version(2)

    def two_to_three(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(messages);")
        result = cursor.fetchall()
        columns = [value[1] for value in result]
        if "limit_to_one" not in columns:
            cursor.execute("ALTER TABLE messages ADD COLUMN 'limit_to_one' INT;")
            cursor.execute(
                "UPDATE messages SET limit_to_one = 0 WHERE limit_to_one IS NULL;"
            )
            conn.commit()

        cursor.close()
        conn.close()
        self.set_version(3) 