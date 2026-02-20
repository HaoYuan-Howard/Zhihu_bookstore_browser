from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
import os
import ddddocr
import shutil
"""
Decrypting Zhihu's encrypted novels
1.Get the mapping table(best cmap) of encrypted char, and save the rendering glyph image 
2.Create the render mapping table of encrypted char using ddddocr
3.Using the cmap to map normal char, but using tender mapping table to decrypt the encrypted char
"""


def export_glyph_images(ttf_file_path, output_directory, font_size=72):
    """
    导出 TTF 文件中的加密字形为 PNG 图片。

    参数:
        ttf_file_path (str): TTF 字体文件的路径。
        output_directory (str): 导出图片的保存目录。
        font_size (int): 字体大小，用于渲染字形。默认值为72。
    """
    # 创建输出目录
    os.makedirs(output_directory, exist_ok=True)

    # 加载字体文件
    font = ImageFont.truetype(ttf_file_path, font_size)
    ttf = TTFont(ttf_file_path)

    # 获取字体的 cmap（字符编码映射表）
    cmap = ttf['cmap'].getBestCmap()  # 返回最佳 cmap 映射 (字形编码: Unicode 编码)

    # 遍历 cmap 里所有字符编码
    for codepoint, char in cmap.items():
        # codepoint是字形编码（十进制），char是Unicode编码(十六进制)
        try:
            # 将编码转换为字符
            char = chr(codepoint)

            # 创建新图像，白底
            img = Image.new("RGB", (100, 100), (255, 255, 255))  # 白底
            draw = ImageDraw.Draw(img)

            # 绘制字形(字符渲染后的形状)，黑色字
            draw.text((10, 10), char, font=font, fill=(0, 0, 0))

            # 保存图像，文件名为 Unicode 编码的十六进制表示
            img.save(os.path.join(output_directory, f"uni{codepoint:04X}.png"))
        except Exception as e:
            print(f"无法处理字符 {char}: {e}")

    # 关闭字体文件
    ttf.close()


def ocr_glyph(output_directory, remove_glyph_image=True):
    """
    使用 ddddocr 识别 output_directory 中的所有字形图片，返回 unicode 编码到识别结果的映射表。

    参数:
        output_directory (str): 包含字形图片的目录，文件名为 unicode 编码。

    返回:
        render_map (dict): unicode 编码到 OCR 识别结果的映射表。
    """
    # 初始化 OCR 引擎
    ocr = ddddocr.DdddOcr()

    # 初始化 render_map 映射表
    render_map = {}

    # 遍历 output_directory 中的所有文件
    for file_name in os.listdir(output_directory):
        # 文件名为 Unicode 编码（例如 "uni4F5C.png"）
        if file_name.endswith(".png"):
            # 提取 Unicode 编码部分，假设文件名格式为 "uniXXXX.png"
            unicode = file_name[:-4]  # 提取中间的 '4F5C' 部分

            # 读取图片文件
            image_path = os.path.join(output_directory, file_name)
            with open(image_path, 'rb') as img_file:
                img_bytes = img_file.read()

            # 使用 ddddocr 进行字符识别
            try:
                ocr_result = ocr.classification(img_bytes)

                # 将 Unicode 编码映射到 OCR 识别结果
                render_map[unicode] = ocr_result
            except Exception as e:
                print(f"识别 {file_name} 时出错: {e}")

    if remove_glyph_image:
        # 删除文件夹及其内容
        shutil.rmtree(output_directory)

    return render_map


def decrypted_md(md_path, ttf_file_path, render_map):
    """
    将 Markdown 中的加密文本映射回 Unicode 编码，非加密文本不变，再通过 render_map 解密文本，并覆盖原 Markdown 文件。

    :param md_path: Markdown 文件的路径，将被解密内容覆盖。
    :param ttf_file_path: TTF 字体文件路径。
    :param render_map: 从 Unicode 编码到解密字符的映射表（OCR 识别的结果）。
    :return: None
    """
    # 1. 加载字体文件的 cmap
    font = TTFont(ttf_file_path)
    cmap = font['cmap'].tables[0].cmap

    # 2. 创建字形到 Unicode 编码的映射表
    unicode_to_char = {}
    for codepoint, glyph_name in cmap.items():
        char = chr(codepoint)
        unicode_to_char[glyph_name] = char

    # 反转映射：从字符到 Unicode 编码的映射表
    char_to_unicode = {v: k for k, v in unicode_to_char.items()}

    # 3. 读取 Markdown 文件内容
    with open(md_path, 'r', encoding='utf-8') as file:
        md_content = file.read()

    # 4. 创建解密后的内容列表
    decrypted_content = []

    # 5. 遍历 Markdown 文件的每个字符，处理加密字符
    for char in md_content:
        # 检查该字符是否在 cmap 中映射为加密字符
        if char in char_to_unicode:
            unicode_codepoint = char_to_unicode[char]

            # 通过 render_map 进行解密
            if unicode_codepoint in render_map:
                # 替换加密字符为解密结果
                decrypted_content.append(render_map[unicode_codepoint])
            else:
                # 若没有对应的解密结果，则保留原字符
                decrypted_content.append(char)
        else:
            # 如果字符不在映射表中，则保持原样
            decrypted_content.append(char)

    # 6. 将解密后的内容拼接成字符串
    decrypted_md_content = ''.join(decrypted_content)

    # 7. 覆盖原 Markdown 文件
    with open(md_path, 'w', encoding='utf-8') as file:
        file.write(decrypted_md_content)


def main(ttf_file_path,output_directory,md_path):
    # main function
    export_glyph_images(ttf_file_path, output_directory)
    render_map = ocr_glyph(output_directory)
    decrypted_md(md_path, ttf_file_path, render_map)

