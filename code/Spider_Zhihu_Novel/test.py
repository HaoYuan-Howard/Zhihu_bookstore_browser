from fontTools.ttLib import TTFont
import unicodedata


def create_glyph_to_char_map(font_path):
    """
    解析TTF文件，创建一个从字形名称到字符列表的反向映射。
    """
    font = TTFont(font_path)
    cmap = font['cmap'].getBestCmap()  # 获取最佳的cmap表

    glyph_to_chars = {}
    for char_code, glyph_name in cmap.items():
        if glyph_name not in glyph_to_chars:
            glyph_to_chars[glyph_name] = []
        glyph_to_chars[glyph_name].append(chr(char_code))
    return glyph_to_chars

a = create_glyph_to_char_map(r"E:\practice_group\generate_novel\material\ttf\zhihu.ttf")
print(a)