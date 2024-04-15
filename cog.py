from discord.ui import Select, View, Button, Modal
from discord.commands import Option, slash_command
from discord.ext import commands, tasks
import discord, json

class LocalToNetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name = "localtonet", description = f"Local Apps to Net")
    async def _localtonet(self, ctx):
        e = discord.Embed(title = "接続の確認", description = f"画面上に表示されている \"接続ID\" を入力してください。", color = 0x33bbdd)
        v = View()
        b = Button(
            label = f"認証する", 
            style = discord.ButtonStyle.green, 
            custom_id = f"localtonet:connect"
        )
        v.add_item(b)
        await ctx.respond(embed = e, view = v, ephemeral = True)

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.custom_id == None:
            return

        if interaction.custom_id == "localtonet:connect":
            m = Modal(
                title = "接続IDを入力",
                custom_id = f"localtonet:connecting"
            )
            m.add_item(
                discord.ui.InputText(
                    label = f"接続ID",
                    style = discord.InputTextStyle.short,
                    max_length = 5,
                    min_length = 5,
                    required = True
                )
            )
            await interaction.response.send_modal(m)

        elif interaction.custom_id == "localtonet:connecting":
            with open(f"./localnet.json", "r") as f:
                data = json.load(f)
                f.close()
            connect_id = interaction.data['components'][0]['components'][0]['value']
            if connect_id in data.keys():
                e = discord.Embed(title = f"接続認証", description = f"画面上に表示されている \"認証PIN\" を入力してください。", color = 0x33bbdd)
                v = View()
                b = Button(
                    label = f"認証する",
                    style = discord.ButtonStyle.green,
                    custom_id = f"localtonet:auth:{connect_id}"
                )
                v.add_item(b)
                await interaction.response.edit_message(embed = e, view = v)

            else:
                e = discord.Embed(title = "認証失敗", description = f"入力された接続IDは見つかりませんでした。\n番号をお確かめの上、もう一度お試しください。", color = 0xfa0909)
                await interaction.response.edit_message(embed = e, view = None)
                return

        elif interaction.custom_id.startswith("localtonet:auth:"):
            connect_id = interaction.custom_id.split(":")[2]
            m = Modal(
                title = f"接続認証 - {connect_id}",
                custom_id = f"localtonet:auth_pin:{connect_id}"
            )
            m.add_item(
                discord.ui.InputText(
                    label = f"認証PIN",
                    style = discord.InputTextStyle.short,
                    max_length = 5,
                    min_length = 5,
                    required = True
                )
            )
            await interaction.response.send_modal(m)

        elif interaction.custom_id.startswith("localtonet:auth_pin:"):
            connect_id = interaction.custom_id.split(":")[2]
            with open(f"./localnet.json", "r") as f:
                connect = json.load(f)
                f.close()

            auth_pin = int(connect[connect_id]['auth_pin'])
            _pin = int(interaction.data['components'][0]['components'][0]['value'])
            if auth_pin == _pin:

                connect[str(connect_id)]['status']['code'] = 1
                connect[str(connect_id)]['status']['owner'] = interaction.user.id
                with open(f"./localnet.json", "w") as f:
                    json.dump(connect, f, indent = 4, ensure_ascii = False)
                    f.close()

                e = discord.Embed(title = "接続成功", description = f"接続ID: {connect_id} と接続しました。", color = 0x33bbdd)
                v = View()
                b = Button(
                    label = f"返答データを編集する",
                    style = discord.ButtonStyle.green,
                    custom_id = f"localtonet:return_data:{connect_id}"
                )
                v.add_item(b)
                await interaction.response.edit_message(embed = e, view = v)
            else:
                e = discord.Embed(title = "接続失敗", description = f"認証PINが間違っています。\n確認の上、再度お試しください。", color = 0xfa0909)
                await interaction.response.edit_message(embed = e, view = None)

        elif interaction.custom_id.startswith(f"localtonet:return_data:"):
            connect_id = interaction.custom_id.split(":")[2]
            with open(f"./localnet.json", "r") as f:
                data = json.load(f)
                f.close()

            products = data[str(connect_id)]['products']
            _options = []
            for item in products:
                a = discord.SelectOption(
                    label = f"{item}"
                )
                _options.append(a)
            e = discord.Embed(title = "返答データを編集する", description = f"返答するデータを選択してください：", color = 0x128797)
            v = View()
            s = Select(
                placeholder = f"選択してください：",
                options = _options,
                custom_id = f"localtonet:return:{connect_id}",
                max_values = len(products)
            )
            v.add_item(s)
            await interaction.response.edit_message(embed = e, view = v)

        elif interaction.custom_id.startswith("localtonet:return:"):
            connect_id = interaction.custom_id.split(":")[2]
            with open(f"./localnet.json", "r") as f:
                data = json.load(f)
                f.close()

            products = interaction.data['values']
            data[str(connect_id)]['products'] = products
            data[str(connect_id)]['status']['code'] = 2

            with open(f"./localnet.json", "w") as f:
                json.dump(data, f, indent = 4, ensure_ascii = False)
                f.close()

            e = discord.Embed(title = "返答データの編集", description = f"編集を完了しました。", color = 0xfafa5f)
            await interaction.response.edit_message(embed = e, view = None)

def setup(bot):
    bot.add_cog(LocalToNetCog(bot))