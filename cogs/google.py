import discord
from discord.ext import commands
import asyncio
from googletrans import Translator
import googletrans

class Google(commands.Cog, name="google"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='translate',aliases=['t'])
    async def translate(self,ctx: commands.Context,*query):
        query = " ".join(query)
        if (len(query)==0):
            em = discord.Embed()
            em.title = f'Usage: /translate TO_TRANSLATE'
            em.description = f'Translates TO_TRANSLATE to english using google translate'
            em.add_field(name="Example", value="/translate Je ne sais pas | /translate こんにちは世界", inline=False)
            em.add_field(name="Aliases", value="/t", inline=False)
            em.add_field(name="Supported Languages", value="af: afrikaans, sq: albanian, am: amharic, ar: arabic, hy: armenian, az: azerbaijani, eu: basque, be: belarusian, bn: bengali, bs: bosnian, bg: bulgarian, ca: catalan, ceb: cebuano, ny: chichewa, zh-cn: chinese_simplified, zh-tw: chinese_traditional, co: corsican, hr: croatian, cs: czech, da: danish, nl: dutch, en: english, eo: esperanto, et: estonian, tl: filipino, fi: finnish, fr: french, fy: frisian, gl: galician, ka: georgian, de: german, el: greek, gu: gujarati, ht: haitian creole, ha: hausa, haw: hawaiian, iw: hebrew, he: hebrew, hi: hindi, hmn: hmong, hu: hungarian, is: icelandic, ig: igbo, id: indonesian, ga: irish, it: italian, ja: japanese, jw: javanese, kn: kannada, kk: kazakh, km: khmer, ko: korean, ku: kurdish (kurmanji)", inline=False)
            em.add_field(name="\u200b", value="ky: kyrgyz, lo: lao, la: latin, lv: latvian, lt: lithuanian, lb: luxembourgish, mk: macedonian, mg: malagasy, ms: malay, ml: malayalam, mt: maltese, mi: maori, mr: marathi, mn: mongolian, my: myanmar (burmese), ne: nepali, no: norwegian, or: odia, ps: pashto, fa: persian, pl: polish, pt: portuguese, pa: punjabi, ro: romanian, ru: russian, sm: samoan, gd: scots gaelic, sr: serbian, st: sesotho, sn: shona, sd: sindhi, si: sinhala, sk: slovak, sl: slovenian, so: somali, es: spanish, su: sundanese, sw: swahili, sv: swedish, tg: tajik, ta: tamil, te: telugu, th: thai, tr: turkish, uk: ukrainian, ur: urdu, ug: uyghur, uz: uzbek, vi: vietnamese, cy: welsh, xh: xhosa, yi: yiddish, yo: yoruba, zu: zulu", inline=False)
            em.color = 0x22BBFF
            await ctx.send(embed=em)
            return
        async with ctx.typing():
            translator = Translator()
            translated = translator.translate(query)
            prediction = translator.detect(query)
            em = discord.Embed()
            em.title = f'Translation'
            em.description = f'Source language: {googletrans.LANGUAGES.get(prediction.lang)}\nConfidence: {prediction.confidence*100}%'
            if(len(translated.text) > 1020): #1024 character limit
                em.add_field(name="Translation", value=translated.text[:1020], inline=False)
                em.add_field(name="\u200b", value=translated.text[1020:], inline=False)
            else:
                em.add_field(name="Translation", value=translated.text, inline=False)
            em.color = 0x22BBFF
        await ctx.send(embed=em)

    @commands.command(name='translateto',aliases=['t2'])
    async def translateto(self,ctx: commands.Context,language="",*query):
        if (len(language)==0 or language == 'help'):
            em = discord.Embed()
            em.title = f'Usage: /translateto RESULT_LANG  TO_TRANSLATE'
            em.description = f'Translates TO_TRANSLATE to RESULT_LANG using google translate'
            em.add_field(name="Example", value="/translate english Je ne sais pas | /translate ar hello world!", inline=False)
            em.add_field(name="Aliases", value="/t2", inline=False)
            em.add_field(name="Supported Languages", value="af: afrikaans, sq: albanian, am: amharic, ar: arabic, hy: armenian, az: azerbaijani, eu: basque, be: belarusian, bn: bengali, bs: bosnian, bg: bulgarian, ca: catalan, ceb: cebuano, ny: chichewa, zh-cn: chinese_simplified, zh-tw: chinese_traditional, co: corsican, hr: croatian, cs: czech, da: danish, nl: dutch, en: english, eo: esperanto, et: estonian, tl: filipino, fi: finnish, fr: french, fy: frisian, gl: galician, ka: georgian, de: german, el: greek, gu: gujarati, ht: haitian creole, ha: hausa, haw: hawaiian, iw: hebrew, he: hebrew, hi: hindi, hmn: hmong, hu: hungarian, is: icelandic, ig: igbo, id: indonesian, ga: irish, it: italian, ja: japanese, jw: javanese, kn: kannada, kk: kazakh, km: khmer, ko: korean, ku: kurdish (kurmanji)", inline=False)
            em.add_field(name="\u200b", value="ky: kyrgyz, lo: lao, la: latin, lv: latvian, lt: lithuanian, lb: luxembourgish, mk: macedonian, mg: malagasy, ms: malay, ml: malayalam, mt: maltese, mi: maori, mr: marathi, mn: mongolian, my: myanmar (burmese), ne: nepali, no: norwegian, or: odia, ps: pashto, fa: persian, pl: polish, pt: portuguese, pa: punjabi, ro: romanian, ru: russian, sm: samoan, gd: scots gaelic, sr: serbian, st: sesotho, sn: shona, sd: sindhi, si: sinhala, sk: slovak, sl: slovenian, so: somali, es: spanish, su: sundanese, sw: swahili, sv: swedish, tg: tajik, ta: tamil, te: telugu, th: thai, tr: turkish, uk: ukrainian, ur: urdu, ug: uyghur, uz: uzbek, vi: vietnamese, cy: welsh, xh: xhosa, yi: yiddish, yo: yoruba, zu: zulu", inline=False)
            em.color = 0x22BBFF
            await ctx.send(embed=em)
            return
        query = " ".join(query)
        language = language.lower()
        if (language == "chinese_traditional"):
            language = "chinese (traditional)"
        elif (language=="chinese_simplified"):
            language = "chinese (simplified)"
        if not language in googletrans.LANGUAGES:
            if(language in googletrans.LANGUAGES.values()):
                for key, val in googletrans.LANGUAGES.items():
                    if val==language:
                        language = key
            else:
                em = discord.Embed()
                em.title = f'Error:'
                em.description = f"Language not found"
                em.color = 0xEE0000
                await ctx.send(embed=em)
                return
        async with ctx.typing():
            translator = Translator()
            translated = translator.translate(query,dest=language)
            prediction = translator.detect(query)
            em = discord.Embed()
            em.title = f'Translation'
            em.description = f'Source language: {googletrans.LANGUAGES.get(prediction.lang)}\nConfidence: {prediction.confidence*100}%'
            if(len(translated.text) > 1020): #1024 character limit
                em.add_field(name="Translation", value=translated.text[:1020], inline=False)
                em.add_field(name="\u200b", value=translated.text[1020:], inline=False)
            else:
                em.add_field(name="Translation", value=translated.text, inline=False)
            em.color = 0x22BBFF
        await ctx.send(embed=em)

    @commands.command(name='translatetofrom',aliases=['t2f'])
    async def translatetofrom(self,ctx: commands.Context,language="",language2="",*query):
        if (len(language)==0 or language == 'help'):
            em = discord.Embed()
            em.title = f'Usage: /translatetofrom RESULT_LANG GIVEN_LANG TO_TRANSLATE'
            em.description = f'Translates TO_TRANSLATE in GIVEN LANG to RESULT_LANG using google translate'
            em.add_field(name="Example", value="/translate english french Je ne sais pas | /translate ar en hello world!", inline=False)
            em.add_field(name="Aliases", value="/t2f", inline=False)
            em.add_field(name="Supported Languages", value="af: afrikaans, sq: albanian, am: amharic, ar: arabic, hy: armenian, az: azerbaijani, eu: basque, be: belarusian, bn: bengali, bs: bosnian, bg: bulgarian, ca: catalan, ceb: cebuano, ny: chichewa, zh-cn: chinese_simplified, zh-tw: chinese_traditional, co: corsican, hr: croatian, cs: czech, da: danish, nl: dutch, en: english, eo: esperanto, et: estonian, tl: filipino, fi: finnish, fr: french, fy: frisian, gl: galician, ka: georgian, de: german, el: greek, gu: gujarati, ht: haitian creole, ha: hausa, haw: hawaiian, iw: hebrew, he: hebrew, hi: hindi, hmn: hmong, hu: hungarian, is: icelandic, ig: igbo, id: indonesian, ga: irish, it: italian, ja: japanese, jw: javanese, kn: kannada, kk: kazakh, km: khmer, ko: korean, ku: kurdish (kurmanji)", inline=False)
            em.add_field(name="\u200b", value="ky: kyrgyz, lo: lao, la: latin, lv: latvian, lt: lithuanian, lb: luxembourgish, mk: macedonian, mg: malagasy, ms: malay, ml: malayalam, mt: maltese, mi: maori, mr: marathi, mn: mongolian, my: myanmar (burmese), ne: nepali, no: norwegian, or: odia, ps: pashto, fa: persian, pl: polish, pt: portuguese, pa: punjabi, ro: romanian, ru: russian, sm: samoan, gd: scots gaelic, sr: serbian, st: sesotho, sn: shona, sd: sindhi, si: sinhala, sk: slovak, sl: slovenian, so: somali, es: spanish, su: sundanese, sw: swahili, sv: swedish, tg: tajik, ta: tamil, te: telugu, th: thai, tr: turkish, uk: ukrainian, ur: urdu, ug: uyghur, uz: uzbek, vi: vietnamese, cy: welsh, xh: xhosa, yi: yiddish, yo: yoruba, zu: zulu", inline=False)
            em.color = 0x22BBFF
            await ctx.send(embed=em)
            return
        query = " ".join(query)
        language = language.lower()
        if (language == "chinese_traditional"):
            language = "chinese (traditional)"
        elif (language=="chinese_simplified"):
            language = "chinese (simplified)"
        if not language in googletrans.LANGUAGES:
            if(language in googletrans.LANGUAGES.values()):
                for key, val in googletrans.LANGUAGES.items():
                    if val==language:
                        language = key
            else:
                em = discord.Embed()
                em.title = f'Error:'
                em.description = f"Result language not found"
                em.color = 0xEE0000
                await ctx.send(embed=em)
                return
        if not language2 in googletrans.LANGUAGES:
            if(language2 in googletrans.LANGUAGES.values()):
                for key, val in googletrans.LANGUAGES.items():
                    if val==language2:
                        language2 = key
            else:
                em = discord.Embed()
                em.title = f'Error:'
                em.description = f"Source language not found"
                em.color = 0xEE0000
                await ctx.send(embed=em)
                return
        async with ctx.typing():
            translator = Translator()
            translated = translator.translate(query,src=language2,dest=language)
            prediction = translator.detect(query)
            em = discord.Embed()
            em.title = f'Translation'
            em.description = f'Source language: {googletrans.LANGUAGES.get(prediction.lang)}\nConfidence: {prediction.confidence*100}%'
            if(len(translated.text) > 1020): #1024 character limit
                em.add_field(name="Translation", value=translated.text[:1020], inline=False)
                em.add_field(name="\u200b", value=translated.text[1020:], inline=False)
            else:
                em.add_field(name="Translation", value=translated.text, inline=False)
            em.color = 0x22BBFF
        await ctx.send(embed=em)

    @commands.command(name='translatefromto',aliases=['tf2'])
    async def translatefromto(self,ctx: commands.Context,language="",language2="",*query):
        if (len(language)==0 or language=='help'):
            em = discord.Embed()
            em.title = f'Usage: /translatefromto GIVEN_LANG RESULT_LANG TO_TRANSLATE'
            em.description = f'Translates TO_TRANSLATE in GIVEN LANG to RESULT_LANG using google translate'
            em.add_field(name="Example", value="/translate french english Je ne sais pas | /translate en ar hello world!", inline=False)
            em.add_field(name="Aliases", value="/tf2", inline=False)
            em.add_field(name="Supported Languages", value="af: afrikaans, sq: albanian, am: amharic, ar: arabic, hy: armenian, az: azerbaijani, eu: basque, be: belarusian, bn: bengali, bs: bosnian, bg: bulgarian, ca: catalan, ceb: cebuano, ny: chichewa, zh-cn: chinese (simplified), zh-tw: chinese (traditional), co: corsican, hr: croatian, cs: czech, da: danish, nl: dutch, en: english, eo: esperanto, et: estonian, tl: filipino, fi: finnish, fr: french, fy: frisian, gl: galician, ka: georgian, de: german, el: greek, gu: gujarati, ht: haitian creole, ha: hausa, haw: hawaiian, iw: hebrew, he: hebrew, hi: hindi, hmn: hmong, hu: hungarian, is: icelandic, ig: igbo, id: indonesian, ga: irish, it: italian, ja: japanese, jw: javanese, kn: kannada, kk: kazakh, km: khmer, ko: korean, ku: kurdish (kurmanji)", inline=False)
            em.add_field(name="\u200b", value="ky: kyrgyz, lo: lao, la: latin, lv: latvian, lt: lithuanian, lb: luxembourgish, mk: macedonian, mg: malagasy, ms: malay, ml: malayalam, mt: maltese, mi: maori, mr: marathi, mn: mongolian, my: myanmar (burmese), ne: nepali, no: norwegian, or: odia, ps: pashto, fa: persian, pl: polish, pt: portuguese, pa: punjabi, ro: romanian, ru: russian, sm: samoan, gd: scots gaelic, sr: serbian, st: sesotho, sn: shona, sd: sindhi, si: sinhala, sk: slovak, sl: slovenian, so: somali, es: spanish, su: sundanese, sw: swahili, sv: swedish, tg: tajik, ta: tamil, te: telugu, th: thai, tr: turkish, uk: ukrainian, ur: urdu, ug: uyghur, uz: uzbek, vi: vietnamese, cy: welsh, xh: xhosa, yi: yiddish, yo: yoruba, zu: zulu", inline=False)
            em.color = 0x22BBFF
            await ctx.send(embed=em)
            return
        query = " ".join(query)
        await self.translatetofrom(ctx,language2,language,query)
        

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        em = discord.Embed()
        em.title = f'Error: {__name__}'
        em.description = f"{error}"
        em.color = 0xEE0000
        await ctx.send(embed=em)
def setup(bot):
    bot.add_cog(Google(bot))