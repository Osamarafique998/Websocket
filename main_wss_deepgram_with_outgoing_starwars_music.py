import asyncio
import websockets
import sys
import json
import base64
import time

import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, NoCredentialsError

base64_encoded_sound_data = "Z2dn////Z///Z////2f/Z/9n////Z2f//2f/Z2f//2dn/2dnZ/9n//9nZ2dn//9nZ2dnZ/9n/////2f///9nZ2dnZ2dnZ2dnZ/9nZ2dnZ2dnZ2f//2dnZ2dnZ2dnZ///////Z2dn//////////9nZ2f//////2dn/2dn//////9nZ2f/////////Z2f//////2dnZ2dn////Z1tn/////2dnZ/9nZ2dnZ2dnZ///Z1tb/////2dnW2dnZ////2dnZ///Z2dnZ///Z///Z1tb/////1tn//9nW1v/5/9nW2fn2/9bU//n/2dbZ+fbZ1Nb/+f/W1v/2+dnW1vn5/9bW///52dn5/9bU1tn5+f/Z/////9bW//b5/9n/9vnW1Nb59v/U1vb52dbZ+fnZ1Nb/+fn51Nb//9nW2f/5/9b5+f/U1Pn5+dnZ+dnZ1vn52f/Z+dnW//b/1NTU//n/////2dTZ///5/9nZ2dnZ2f/W1v/5+dbU2f/5/9nZ///5+dnZ1vbZ2dnW9v///9bZ2fnU1v/Z9vnZ1P/52dn/1v//2f/W+fnZ1tbZ/9nZ+fb52f/W1vnW9v///9b2/9bTU1n59tnZ+dnZ1NT///b52dnW+dnZ2dn52dn/2f/Z2dn5/9nZ/9nZ///Z/9b///nZ1v/2/9bW2f//2f/5+dnW2db/2fn0/9bU2f///9nW+f//+f///9n/2fn22dn5/9nZ/9T/+dnZ2dT/+fnU03///9nZ+dn52dn52f/W///59v//1v/5/9bW+fn//9n5/9bW/9nZ1v///9bW2dnW1tb5///Z2fnZ2dbZ+f///9n5/9nZ//n/2f//9tnZ1NN//9nW1NnW/9nW2dbZ2f//2dn/+fnZ///5+fn0+fb5+fb29v//2dbZ01JTVNbSUVNU1NNTU1b/+f//+fNzc3NzcnJwcHFxcnFxdPb50U4OkVFPjgyODg4PDxBTf/T09vTwby6vryytLS4urq6vMXbSTo6Pjw2LikoKC0uOkVJW2fNxcHBwbKtra6wr6+yuL6+wdNbPjw8Ni4qJSQlJS1JZ1tJTdvBvL64tK2rsLK4tLS4uLq6xedNPjQwLiolHyIkMGf//0lJZ9O+tq+rrK+yuLy+uLa0srjB0004Mi4sKiUfHyQ2yb5nODZNzcG0rqWosLS+vMG+trKvtrrB/zYqJykrJyAfJ1u2zTotNGfNwbapoqqwury8xcG6sK2vuMlFLiYmJysmIR80vLxNLS5F083FrqWiq8G8vLrFxbauqbLF/zotKCQmJh8eKbqw0y8nOufb27akoqS4wbzBvMm4sKuqts1BLikkIyIeHSe6qsUwJTRn/1u8paCnsMXFwcHBvrCsq7DJUzQpJCIjIB0jvqi0MiMy/9NTzamgorTTxb6+vM26raqvxVs6KiIhJCIeI82ptDQiL+fTW8Goo6WvycXBwbjFwbSrq7z/NCYjIiIiHie4rMEtITL/2+e2paOktNPBvr7Fvravr6+6/y8jISMjIB00rKpbJCQ8/+fnr6Cfp8nnxbrFwbq4r6uvxUEpIiAfIB0kwaawMiYuSVNJwaeen7Lbyby6vMnFsqyrtmcwIx8eHx4f/6iwUycvRT4+56qgoK7BvLq6xcnJtK2ustsyIx8fIR4fSaqwRScsZ9s+/6+hn67Fuq+0wVPbr6uuwWcvJSIfHx0izau4NiU201tFxaifqLq6r7LBxdO4ra+2vEUoIiAjIR0rtKrTKSZF01tbtp+gsry8rrLB076srrLJQSsmJiQjHiLnrbw4KTRn21u+p6OrtK6yrsHbvrawtME8KSgpKiAcIluywTgvOv/nZ7ytpqutqq6wxcnBuLi6xTYrJSknHh0n57znODRJZ2fTuKyrq6utq7a6wcW4uMFBLyssKyEdHi/b01M6PFPn/8mwramor6+0uLq6uri8ZzQsLC4oIR4mRVtbTTxJZ+fFtLCtp6qvtrawtr7Fxds8LCsvLCMfIjhNTVNFTWfnxbSwrKirrq+vr7K6xclNLy0uLSolJCYvPEFnSU3byby2sq2sra2urq+0usHbNi8yLy0oJSUpMDpJZ01Tzb66tK+vrq2trrCytLjFUzIwMi8tJyYmKzI2SVtb58W6uLSvr66ura2wtLrB50EyMjQtLCgkJy02OltTW8m+vLqwrK6urq2usLi8yec6LjIvLCsnJScsNkVnW2e+xb6ysK+tra6tr7C2usX/PjI0LS0rJSYlLDJBU1vnxcHFtLCvrKutrq2ytrzF2zwyNDItKikjIyovOltn/8nBxb6yrqysq6yvr7K2vslbOjIyLispIyUoKC8+W2f/vr7BuLCvr6yrra2utri8zWc6ODgtLComJCUmLDpJW9vBwb66tq+urqyrrq6usrq+yU04NjQtKyolIyQlKjZFU9vJzcm6tK+qqaqtra+ysrK0vMVbODg0KisqISIiIigyRU3nwc3Fvry0raqpqq6usra0tLq8wVs8ODIrKichICEhJzZFSee+08W6urKtq6qqq66wsra6tra8yWc6NC8qKiYhIiAgIy8+Ps28zcG4wbqrrKyoqq+ysrq8tra8wclNOjouKSgnIyEjIiUwPEnJxc2+usG6rq+vqKyyrLa8ury4uri+01tBNi4sKCYlIiIiJS82ScW+xb7BzcW4srStr76ytMm2ssG4srq6tMVnUzovLismJiQhISEtMjzFzc28wefJvNO4sK+vsK7BvMHBvrqvvLKyxb7JW0E8NCwuLCgnJR8eJysy083bwc1b08XJvLC0trK6urjJtsnFtsm6uLq4vLjFzcVbW1s4OjIrKSMgHiQqLVNbW83/Z+fN28G6wbq6wcHBycW4vLiyuri2vL64wcW+ydPN02dTPjQuKyUhHx0kJC5TQdPF/9vJ28m6vrq2ur6+xdvJ283Fxb68vr6+xb7Bwb6+vL6809P/SUk8NjArJSAeIiIqPjjnzf/BwcW8uL68usG+wcnNydPNzdPb09Pbzc3Tzc3bwcHBury8xcXT5/9FPDQsJyQeHyIjMDhB29vbvsnFuL6+usHBwcnNydPNyc3FydPT09vTzc3JxcHBvr7BvL6+vsnN52dFPjYuKyUhHiIhKDYyU+dnwcG+uri8vrzFxcXbzc3Tyc3NydPT0//n/2fn59PJyb6+urq6ury8xcnTZ1NBOjQtKigiIickLzY4/2fnxcXBurq8urzFwc3Tzdvb09vT09vb52f/W1vn/83Bwb66vry4vrq8xcnb/1tJQTo0LywpJiMjJycwOD5n/9PFvr64uLq6ur7BxdPN29vT29vT5+fnZ/9n/+fbycG+urq8ury8usHFzedbU0E8ODAvLSooJSYoKjQ4Rf9nzcXBurq8ur7BxcnT29vn09PTzdPTzdvn2+f/083NvsG+vMG+vL6+xc3bZ1NNPjw4MjAuLCwoKCwqMjo6W1tnyc3FvLy+ur7BvsXNydPTzdPTzdPT0+fb5+fb083FwcG+wcHBxcXF09vnU1NJPj46NjQwLy4rKywsLzY4QVNT283Jvr68ury8vsHBycnNzc3TzdPT0+fb5+fb083FxcHFxcXJyc3T2+f/W1tNSUk+Pj44ODgyMjAuLzAyNDw+SVtn28nJvry8vLy+vsHFyc3J09PN29PT29Pb083NxcnJxc3JzdPT2///W1NTSUVBPjw6ODg2NjY0NjY4Oj5BSVtn59vTycnFwcHBwcHBxcXFxcXFxcXJycnNzc3T09vb2+f//2dbW01NSUVBQT48Ojg4ODg4ODo8PkFJU1v/59vTzc3JycnFxcXFxcXBwcHBwcXBxcnFyc3N09vn5/9nW1NNSUVFQUE+Pjw8PDw8PDw+PkFBRUlNU1NnZ//n59vTzc3JxcXBwcHBwb6+wcHBxcnJzdPb5///Z1tbU01NSUVFRUFFQUFFRUVFRUlNTVNTU1tbW2dnZ2f////n5+fb59vT083TzcnNycnNzc3Nzc3T09vn5///Z1tbU1NTTU1NTU1NTU1NTU1NU1NTU1NbW1tbW2dnZ2dnZ2f////////n5+fn29vb29vT09PT09vb29vb5+fn////Z2dnZ1tbW1tbW1tbW1NbW1NbW1tbW1tbW1tbW2dnZ2dnZ//////////////////n5+fn5+fn5+fn5+fn5+fn/////////2dnZ2dnZ2dnZ1tbW1tbW1tbW1tbZ2dnZ2dnZ2dnZ2dnZ/////////////////////////////////////////////////9nZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2f/Z2f/////////////////////////////////////////////////////Z2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dn//9n//9n/2dnZ2dn//9nZ2f///9nZ////////2dn/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////2dnZ/9n/////2dnZ2f//2f/Z2f/Z/9nZ/9nZ///Z2dn////Z2f/////Z2f//2dn////Z/9nZ2dn////Z2dn////Z2dn/2f/Z/9n/2f/52dbTf/b0+dNU1tn51Nn/9vTW01TW9P//1tn5/9nW//N52dbW+f/Z///5/9nZ2dnZ/9nZ//n5/9bW2f/////Z2f//2dn////52dnW2f///9nZ2f/Z2f/5/9n/2dn/2f/Z/9nvMH/QThT28nTU8W+ZzopTcG6yTxBZ1vbRVv/29NTU1tn22f/Z//TZ2db/9Pb22dbZ2f//2f/W///2+fnW76n5zYnPri000FJZ01FQf/JydNFPDxNzcXbSUVbzcGvq6vFPDzbtsFbRUE8LicmKy8pIx8ropyoNiFBuKutraartv9J28m+yefNzby+xcXF51tb077NZ0U4NDI2Ni8oJB8gG9ufoMElLFuyuLynpq7JQVPnvLbB0//TwbbB001nzbzNZ2dJNjAuLysmKiYjGCOinaUyJ022uM2tn6WyTVPb576wuMVb27jB01Pbzf9TW2f/TUEyLi0nKispIhhTn6CyLTbJvs24o6GyxWfbTf+ysL7/Z8G+51u+vM1NTVNTQTIwLywuKygiIxswpKe0STzbxdu2p6KvtsXT/1u4rcHF2822zc3TzdNb29tTOjAyLi0sKSckHhsup6K4PFPB01O8p6OwtLa8Uzi4rLq8wbrF59vnydP/21tBLystNC0mKCMkHR28n6TNQdPJTcWroa62rbbnQVOytP+8trrT583b0///zUlBPC4qKisrKiUiIB3NpbDN07jbPsGrqbKwp7JTOtuytmfTq77nyefNzefT21NNRTwyJyctKSYlJh0guq20vLq4TVO0qqy0qqbBZ03FsufnsLjT08G+Z+fJyf9BSTwvKiksKCQoJyMaKquyvry0ulPJraywtqmnxVvn58XFxbTBzcXFydPN0+f/W0U4MC4sLCsmJyQjHSO8vMW2tLLT07Swr7Krq7rNzcnBycW2xdPFwcXJwcn/W1NJQS8qMC0nJSglHxwf/8XnuK2yxcGvr7i2ray0wbzBycnJtsXbwcXJwcXJ201NSTwwKy4vKSgoJyMfHjbnZ8Wwr7K8tKqwuLKtrbzFwcnJ28G6ydPNxcnb29P/TUlFQTYvMjYvLC0tKiYlL0VJTefJvsG6sq6wtLSytrzFwb7Bxc3JycnBvsHByc3b52dbSTw2Mi8tLCooJiMkKCwuMjxN2762r6yqp6amp6mqrK+0urzBydPb5/9bTU1JQTw4NDAvLiwqKCclIyYsLzQ8Sdu+tq6rqaenqKiqrK+0uLzBxc3T5+fn/1NNSUVFPjo4NjIvLSsqJyUmKy4yOD5T07y0rqupp6epqauusLa6vMHJ09vn//9nW01JRUU+ODQyLywrKSclJCcsLzQ8See+tK6rqaenpqeprbC0uLzBydPb5+f//2dbTUlFPjo4NDAvLSspJyYnKi4yOEFb07yyraupqKenqKyvtrq+wcnT2+fn5+f/Z1NNSUU+OjYyMC4sKignJigsLzY8Sf/FuK+sqqmop6iprbK4vMHFydPn//////9bTUlFQT46NDAvLi0rKignKS0yOkFN/8W4rqupqKioqauusri+xcnT5/9nZ////2dnZ2dbU0U8ODIvLSsoJiUmKCsvOEFbzbqwrKqoqKipqq2wtrzFzdvnZ1tTU1tbW1tbW1tbU0k+ODQvLSsqKCcmKCsuNDxN276yraqop6eoqauutLrBydPnZ1tTU1tbZ2dnZ2dnW01FPDYyLy0rKScnKCotMjpFZ8m6r6uop6enqKmsr7S6wcnT52dbW1tbW2dnZ///Z1tNRU04LS0tLSwpJyksLzI6RWfNvLKuq6qpqaqrrbC2vMXN2/9nW1tbW2dnZ2dnZ1tNST46NjIvLiwsKyssLjA0PEln0762sK2rqqqqq62vtLi+xc3b/2dbW1NTU1NTU1NNSUU+Ojg0MjAvLy4uLi8yNjpBTWfTvrayr62srK2tr7K2ur7FzdvnZ2dbW1NTU1NTTUlFQT48Ojg4NjY2NjY4ODo8PkVNZ+fNxb66trKysLCwsrS4ur7FydPb52dbW1tTTU1NSUVFQUFBPj4+Pj5BRUFBRUVJTU1NU1tn/+fb083NycXBwcHBwcXFyc3T0+fT01Nn/1NTW1NNU0lJTUlJTUlJTUlNTUlTSVNTTWdbZ2f//9vn09PnyefTzefb0+fnzWfn01vb///nZ+fnU/9bZ+db51tTzVNJ50FTTUlJU0lT/0nTU9vNZ83T5+fJ59vN/9PnZ+dnZ/9nW1tnW+dJ5/9J2/9b5/9T21tb00XbW1PbTf9bZ1vnTdNbZ9tbZ81N0+dTyU3TZ///21P/503TU2f//1P//1tb//9N5+db52fnW1vnW1PbZ1vbW9v//9tb22fnW9tT52dnZ9tJ01tb00nbW2dnZ1PTSefnU+dT21Nn203bTdv/U9vTQcX/U8lT02dn5/9TzVv/51vbU+f/W+dT20nFW9PT/0XTPOdTQc08W80801tnzU3N///JU//BPL5J01Nb203bZ1tnzT7FRdNNyUnNU+dnW//nSf/TPslb/1PJTdNN22fTTdNn50XJ/0XJSf/NRefTPMVJ0+dT580+2+dNZ81F59tN20nT/0HBWz62Os3TPMnNOLhJ5/9nZ81F2+dbZ+dn5+dNzU3TTefnSVvFPsn/Tc1J52dT5+dNwUHb51NbyUn/52fb503T/01n21tT//9T01Pb52fn503NU1vnU1vnTf/nSefTSdvTW9vbU9v/TefbRf//TdNJ/8lJZ9NN51tT01NT5/9T52f/5/9bzVtnzWf/2+fn/9vb/9v/29tn59tTZ9NTW/9TU1tJTU1BQUk+PkE+QUFFRVtbW83BybiytLCvsq+yurjB29NnTVtFPkU8Njo4NjQyMjIyLjI0LjQ2OufTzbStr6ypqKqsrrC6zdtnQVNTRVv/Z2fb52fb/1NTRT4+OjQ6Njg4NjQyMjIwLzJnzdu8ra+vqqirrLKywVtJWz46Z9P/28XBxcHJzedbW01BQUU+OjY0ODgwLy8rKSooLf/Fza+jqqunqa6wurrJST5TSUFT077FzcG4yWfT00lN/2dbTU3nUzQyPDgsKywpJCQmK2e+wbalqq+urK2wydPN/0ln52fbwb68uMHb29tTRWfnU03/2/9b/2c+NjQwLSoqKykmKSo+urK6rKWqr7awrbxnzcH/U+fT22fTwb7NZ1vn51NT/+f/Z+fNydtnTU08Ly4yLioqLCoqKTTFsry2qquttLqyr8nnzclbTVPn2+fbzc3Jzdvbzf9b/9Pb/2fb0/9TSTw2MC8vLiwqKSoqJzLBr7S0raqqsLawr7zT/+fb22f/583J0//TxdP/Z2f/5///29vb/1NNST44Mi8vLi0sKyoqKDLFrrCwrayorLa8trrBZ0lT0+dbTf/Nydv//9vT0+dn59PT51Nb5+dNQTo4ODQyMC4rKysqKTTNrqussK+qq7C6vsXB01tNU//T0///29vN0/9n083T5///2+dTW1tTTUE6NjY0Mi4tKygoKSxFuquqrbSyrKywutPn09PnZ1tn283N0///08XJzednZ//n52dbZ/9bU0U+PDw6NjAsKioqKiguZ7KpqK60tK6trrrnU2fbzdtbU1vbycnbZ1vnycHJ51NTZ+fb52dTTVNNST44NDQwLy0sKyoqNP+2q6mttLi0sK60xWdNU+fT2+dbW+fNxcXN2+fb09PbZ01NTVv//2dTTUlBPDg0MC8vLy8uLTBBzbSsrK+2urqysLa+21NNU2fn5///59vTzc3N0+f//2dnZ2dn////Z1tNRUE8ODYyMC8vLy8vNEXTuK+usLa6ura0trzNZ01NU2fn29vb29vTzc3N2/9nW1tbZ2f///9nU01JQTw4NDIyMjIyLy4yQdu6sK+wtrq6trS0usXnW0lNW+fTzdPb5+fn29vb5/9bU1NbZ+fb52dTSUE8Ojg2NDQ0MjAvLzRF27qwr7C2urq4tra4wdNnTU1b/9PN09Pb29vn5+f/Z2dnZ2dn//9nW1NJPjo4NjQyLy4uLi82Sdu6sK+wtLi4trS0uMHbW0lNW+fTzc3T5+fn59vb5/9bW1tn59vnZ1NFPjw4NjQwLy4sKysuOme+sK2usri4tLKwtLzTW01T/9PFxc3b59vTzc3TZ01JU2fn29v/U0lFPjo2MC4tLSwrKSkwScWvqqyyurq0rq6yxWdNU+fNzdPb29vTycnN21tTU2fn/1tTW2fn51tFNjAwMjIvLCciIi//squtur66r6qqr7znZ+fJxc3/W+fJvrzNW0VJ28HNW0VFU9vN02dFODg4OjgyLCoqKyYoOsmuqrLFwbiuq7TN0828vM1bW+fFvMHbW1vbzf9JRWfb22db/9PTZ0E0MDI2NjArKCgoJzjNtrK2wbawtLS4vri4usHN28nFyedn28XNZ01bZ/9nW1P//+fn0+dTOjAyOjgyLCknKSYpW7q2ur64rrrJtq+wsL7BvL7n5+fN0+fn09tnRU3//2f//9vb59PTZ0k8ODQ2NDAsKicoJSfnusm6sra2xcGtrri2uLjF29PF0//nybzbRVv/TUlT283/Z9vb///n/z4yNDYwLSwsKiclJOe0zbyttrzFuKuvuq2wwc3Fvsln277N/9v/Z0lJZ1tT5///5//n21NnUzg0NC8vLSooJiYjOrbNway2zby4r7K4q6zJxbrB29vJxWfTyVtTW1tnW03T51vT2//nW1NJODo0Li8tLSokKSYovr7br62+uriwsLitqr6+ur7J/83J/8nJU1tbTUlTZ+f/5///29vnZ00+PDYyLywtKiUoJCTFxduursW8uLSytK6rvr68wdPb29PNydP/U01NSVvb/+fn/2f/2/9bUzw8NjAvLSopJiglKLjJ06uy07q8tLCyrK7Btr7Jzdvbyc3J51v/SUVnU//n59P//+f/Z1tBODwyLy4uKikoKiQuuNvBqrbFurq0trCqsri0wcnN283FydNnZ1M+SWdbZ//b/1vn/2dnW0E6ODYwLi8qKScpIzy6W7atxb66tq+yraq0vLjFyc3TvsHT01tJRUFNW1vn2+f/5+fnZ/9bPDw4MjAyLSorKScjZ8FNrrTNuL60sLSrrbq2usHN083FycnnU1NFRVNnW+fnZ+f/Z9NbU2c8NDoyLi8sKygoKSXnyVuttsm2vrSwsKqutrS6xc3TycnFyf9bWz5JU1NT52dn5+f/0/9TUzw2PDYwLisqJSkpJ+fFW7C2zbq6tLCvqa62tLrJ083FxcXJZ2dTQU1JW/9T5/9b09v/22dTOjg+MDAvKyooLCgm581nsLTTuryysrCpr7q2vsXTzc3JwdtbU1tFQVtbSVPbZ1vb/83nZ2c+Ojo4MjAuLCgqLCI6vFu6rsXBwbiwtqyqtLi2vsnNzc3Jwf9bU1tJRednRednW+f/29NbZ0k8Ojo4LzAvKCoqKChJwdO6sr7FvrCysKystry4vs3TzdvTyf9nW1NTRWdTTWdnZ2f/59vnZ01FPjo0NDIuLS0oKSQ6vGe6rcG8vLawuK6tsLzBvtPnzefNxWf//01nTVNnW2f/W2fb5+f/W+dFPD46MDIyLCoqLCgovL7/sLLBvLqutLisrb7FvMFn/8Fn083/00lN20lbZ1v/U1vnZ9PbZ/9JRTw6PDA0Li0rKSwlMrjNwbK8vsG8sLayrLK8xcXF5//N59vT2+dnU01T/2dT/1NTZ9vN29PbTUE8PDg0NDAuLCwrJiy+vM24tLzF07CwuK+stMXnvtNN583BzefN501bW+dnTVtnRVvbzdv/zVs8PDo6NDYyKywrLCwmZ6/Jvra+vue4rLa0r7K8Z8HBZ2fTxc3/29P/TUln52dTW+dnW83Fzef/U0E8NjY0MC0uLS0rKCrTuMG8usXB57qtsLKusr7bycnb59PF2//b51tJTedn/1tTW2f/09PN02dNTT46ODIyNC4wLScpKjq6vLy8wbzNza+tsLK0tMn/xcnT29vFzf/n/2dNU///U0lb////08n/U1NTRTw4OjIyMC8vLiosK026vsG+vrbFvq6tsrS4uMHTycXT0+fTzWdb/2dNSUX/51v/2////9PN/1NTRT44NDY0NDQwMC0rLTrbyc3Jxb66xbausrC0vLa+zcnb59PNzc3b/+f/W1tn/+f/Z2dNSUVFTVNNU01JSUk+Pjo2NjIwMC8uND5FU+fJvrq0rqutr66vsrS6wcnT09vn52dnW1tnU01NSUlNSUlJRUlNTVNNSUVBPj46NjQwLi4yOkFNZ9PBvLavra2ura6wtrzByc3b2+fn//9nZ2dbU1NTU1NTU1NNTUlJSUU+Pjo4NDAvLiwsLjI6QU3/yby4sq+trKytrbC0usHFzdPb5+fn5///Z/9bU1NbU1NTU1NTTUlNSUlBPjw6NjIvLiwrLjQ6QU1nyby4tK+tq6ytr7K0ur7Byc3T/9vb09Pn52dbU1NTU1NTTUlJSUFBQTw6NjQwLSwsLCsqPP/NwcG8uL66trCusrS4vL7J09PT09vn09Pbzc3J0+f/Z2f/Z2dnZ/9bTUU+Pjo4NjIyLi0tLS4sLEXJvrzBvri+vravrrS8urzF09vNzdPb09Pn59PJzf9bW2f////n5/9bTUVBPDw6NjQwLy0sLi0tKjbJvLrBwb7FvrSvrbS4tLzF2+fN29PbycnnZ2fnzdv//+fn/1vn2+dnU01JST4+QTo0MC8vLi0uLisu27y4wdPJwcW6tK2utrq8xdtn283N09vT0////9vb/+fb09tnZ+fb/1NbW01FPjw6ODQyMi4tLS0vLVPBvr7b08XFvLavsLa8wb7N09vbzdvb09Pb////5+fn2+fb5////+fb/2dbU1NJPjg2NDIvLi8wLTAtQcnBvtvNxcW+vLCutr7BwcHT583Tydvbzef/Z2f//+fb59v//+fb2//n52dnU0lNQT44NDIwLi8wMjAvMP/BvMXnycG+vriwsrS+vsHJ29vTzdPT29vbZ1tbZ+fb/////+fn/+f//1NTU01FPjo4NjY0MC8wMjIyMFvBuMFn08W+urqysLS4wb7T0+fTyc3b51vnZ/9nZ+fb2/9n/+fT2///Z2dnW01JQT46NjQ0MjIvMjY2NjJnxbzF28XBuLq4sLK0vMXFyc3b29PT5+dn//9nZ2f/2+fn///n5+f//+f/W01JSUE+Ojg2NDIyMjI2NjQ0W8W6vtvJwbq6urKwsrq+xcnN29PT0+f/////Z+f/5+fn///n5+dn/2dnU0lJSUU+Ojg6NDYyMjQ0NjY2Ps3BuM3Nxb64uri0tLS8wcXNzdPT29vn//9n///n////Z/////9n52dnU01NSUVBPDo4NjQ0NDQ0ODY4POfFvM3Txb64vLa0sra8wcXFzdPT09Pb////Z+dn////5///W2dn5+dnU01JSUU+PDw6NjY2NjQyNjg8OFPTvsHNxcW6vLq2tLa4vsHFydPT09Pb5+dnZ//b0+dnW1v/Z2dn//9bU0lFRUE+Ojo6ODg2ODY4ODg6PGfTxcnNwb68vry2tLa6vr7Fxc3T09Pb5+f//9vb2/9nW2dbZ////1tNRUVFRUU+PDo6ODg4ODg4OjxBRVvbzcXNxcG6urq4uLi6vr7FxcnNzdPb29vT5///Z/9bW1tnW1NNTU1JRUVFRT48PDw6Ojo6Ojw+QUVJU//TzcnFwby8urq6ury8vsHFycnJydPb2+fb/2dbZ2dbW01NSUVJSUlFQT48PDw8PD48PD4+QUVFSVPn29PNxcG+vr68urq8vLy+vsXFyc3N29vn52dnW1NTTU1JSUU+Pj5BQT48PD4+PD5BRU1JSU1b/+fb08nJxcG+vLy8vL6+wcHFycnJzdvn////W1NNSUlFRUFBQT4+Pj4+QUFFSUlJTU1TW2f//+fb083Nyc3JycXFxcXJxcnJzdPT09vb5/9nZ1tbU01NTUlJRUVFRUVFSUlJSU1TU1tbZ///5+fn2+fb09PT09PT09PT09PT29vb29vn5+fn//9nZ1tbU1NTU01NTU1NTU1NTVNTU1tbW2dnZ2f//+fn5+fn2+fn29vb29vb29vn5+fn5+f///////9nZ2dnW1tbW1tbW1NTU1tbU1tbW1tbZ2dnZ2f/////////5///5+fn/////+f///////////////////9nZ2dnZ2dnZ2dbW1tbW1tnZ2dnZ2dnZ2dnZ2f/Z////////////////////////////////////////////2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dn/////////////////////////////////////////2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dn/2f/////////////////////////////////////Z/9nZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dn/////////////////////////////////////2f/Z2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dn//9n////////////////////////////////////////Z2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2f/////////////Z////2dnZ2f/Z/9n//////9nZ/9nZw=="


def linear_to_ulaw(sample):
    if sample > 32767:
        sample = 32767
    elif sample < -32768:
        sample = -32768

    sample = sample + 32768
    exponent = int(sample // 2048) + 33
    mantissa = int(sample // (2 ** (exponent - 33)) - 31)

    ulaw_byte = ~(exponent << 1) & 0xFF
    ulaw_byte = ulaw_byte | (1 if sample >= 0 else 0)
    ulaw_byte = ulaw_byte ^ (0x55 if mantissa & 0x10 else 0)

    return ulaw_byte

def deepgram_connect():
    # Replace with your Deepgram API key.
    extra_headers = {
        'Authorization': 'Token 28cf7294bbf4f397dc7a5e48abfb88bc7518d04c'
    }
    deepgram_ws = websockets.connect(
        "wss://api.deepgram.com/v1/listen?encoding=mulaw&sample_rate=8000&channels=1&endpointing=190&type=enhanced",
        extra_headers=extra_headers)

    return deepgram_ws


async def proxy(client_ws, path):
    # inbox = asyncio.Queue() # not needed unless sending ws messages back to the client
    outbox = asyncio.Queue()
    print('started proxy')
    
    # use these for timing
    audio_cursor = 0.
    conn_start = time.time()
    stream_sid = ''

    async with deepgram_connect() as deepgram_ws:
        async def deepgram_sender(deepgram_ws):
            print('started deepgram sender')
            while True:
                chunk = await outbox.get()
                print("sending data to deepgram for transcription", chunk)
                await deepgram_ws.send(chunk)
            print('finished deepgram sender')

        async def deepgram_receiver(deepgram_ws):
            print('started deepgram receiver')
            nonlocal audio_cursor
            nonlocal stream_sid
            async for message in deepgram_ws:
                try:
                    print("received message back from deepgram_ws", message)
                    dg_json = json.loads(message)

                    # print the results from deepgram!
                    transcript = dg_json['channel']['alternatives'][0]['transcript']

                    if transcript:
                        print(f'Transcript = {transcript}')
                        # print("Sending tome to stream_sid ", stream_sid)
                        # # Set up the Amazon Polly client
                        try:
                            polly_client = boto3.client('polly', aws_access_key_id='AKIAV4ZAFTNKD7AG37FL',
                            aws_secret_access_key='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',region_name='eu-west-1')  
                            # Update region if necessary


                            polly_response = polly_client.synthesize_speech(
                                OutputFormat='pcm',  # Use 'pcm' format for raw audio data
                                Text=transcript,
                                SampleRate="8000",
                                VoiceId='Joanna'  # Change to the desired voice ID
                            )

                            if polly_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                                pcm = polly_response['AudioStream'].read()

                                i16_samples = []
                                for i in range(0, len(pcm), 2):
                                    i16_sample = int.from_bytes(pcm[i:i+2], byteorder='little', signed=True)
                                    i16_samples.append(i16_sample)

                                mulaw_samples = [linear_to_ulaw(sample) for sample in i16_samples]
                                base64_encoded_mulaw = base64.b64encode(bytearray(mulaw_samples)).decode()

                        except NoCredentialsError:
                            print("Amazon AWS credentials not found.")
                        except BotoCoreError as e:
                            print(f"An error occurred with Amazon Polly: {e}")
                        except Exception as e:
                            print(f"An error occurred: {e}")
                        
                        await client_ws.send(json.dumps(
                            {
                                "event": "media",
                                "streamSid": stream_sid,
                                "media": {
                                    "payload": base64_encoded_mulaw
                                }
                            }
                        ))



                # do this logic for timing
                # NOTE: it only makes sense to measure timing for interim results, see this doc for more details: https://docs.deepgram.com/streaming/tutorials/latency.html
                #					try:
                #						if dg_json["is_final"] == False:
                #							transcript = dg_json["channel"]["alternatives"][0]["transcript"]
                #							start = dg_json["start"]
                #							duration = dg_json["duration"]
                #							latency = audio_cursor - (start + duration)
                #							conn_duration = time.time() - conn_start
                #							print('latency: ' + str(latency) + '; transcript: ' + transcript)
                #					except:
                #						print('did not receive a standard streaming result')
                #						continue
                except:
                    print('was not able to parse deepgram response as json')
                    continue
            print('finished deepgram receiver')

        async def client_receiver(client_ws):
            print('started client receiver')
            nonlocal audio_cursor
            nonlocal stream_sid
            # we will use a buffer of 20 messages (20 * 160 bytes, 0.4 seconds) to improve throughput performance
            # NOTE: twilio seems to consistently send media messages of 160 bytes
            BUFFER_SIZE = 20 * 160
            buffer = bytearray(b'')
            empty_byte_received = False
            async for message in client_ws:
                try:
                    data = json.loads(message)
                    if data["event"] == ("connected"):
                        continue
                    if data["event"]  == "start":
                        print("Media WS: Received event start")
                        start = data["start"]
                        stream_sid = start["streamSid"]
                        # print("streamSid derived from start is ", stream_sid)
                        # print("Sending ", json.dumps(
                        #     {
                        #         "event": "media",
                        #         "streamSid": stream_sid,
                        #         "media": {
                        #             "payload": base64_encoded_sound_data
                        #         }
                        #     }
                        # ))
                        # await client_ws.send(json.dumps(
                        #     {
                        #         "event": "media",
                        #         "streamSid": stream_sid,
                        #         "media": {
                        #             "payload": base64_encoded_sound_data
                        #         }
                        #     }
                        # ))
                        continue
                    if data["event"] == "media":
                        media = data["media"]
                        chunk = base64.b64decode(media["payload"])
                        time_increment = len(chunk) / 8000.0
                        audio_cursor += time_increment
                        buffer.extend(chunk)
                        if chunk == b'':
                            empty_byte_received = True

                    if data["event"] == "stop":
                        print("Media WS: Received event stop")
                        break

                    # check if our buffer is ready to send to our outbox (and, thus, then to deepgram)
                    if len(buffer) >= BUFFER_SIZE or empty_byte_received:
                        outbox.put_nowait(buffer)
                        buffer = bytearray(b'')
                except:
                    print('message from client not formatted correctly, bailing')
                    break

            # if the empty byte was received, the async for loop should end, and we should here forward the empty byte to deepgram
            # or, if the empty byte was not received, but the WS connection to the client (twilio) died, then the async for loop will end and we should forward an empty byte to deepgram
            outbox.put_nowait(b'')
            print('finished client receiver')

        await asyncio.wait([
            asyncio.ensure_future(deepgram_sender(deepgram_ws)),
            asyncio.ensure_future(deepgram_receiver(deepgram_ws)),
            asyncio.ensure_future(client_receiver(client_ws))
        ])

        client_ws.close()
        print('finished running the proxy')


def main():
    # use this if using ssl
    #	ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #	ssl_context.load_cert_chain('/cert.pem', 'key.pem')
    #	proxy_server = websockets.serve(proxy, '0.0.0.0', 443, ssl=ssl_context)

    # use this if not using ssl
    proxy_server = websockets.serve(proxy, 'localhost', 5001)

    asyncio.get_event_loop().run_until_complete(proxy_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    sys.exit(main() or 0)
