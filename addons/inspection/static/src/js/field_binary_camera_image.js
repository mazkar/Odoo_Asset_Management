/** @odoo-module **/

// Impor komponen yang diperlukan dari Odoo framework
import { registry } from "@web/core/registry";
import { FieldBinaryImage } from "@web/views/fields/binary/binary_image/binary_image";

// Definisikan widget kustom Anda
export class FieldBinaryCameraImage extends FieldBinaryImage {
  // Tentukan template QWeb yang akan digunakan widget ini
  // Kita akan menggunakan template standar FieldBinaryImage dan mengoverride bagian tertentu di JS
  static template = "FieldBinaryCameraImage"; // Nama template QWeb yang akan didefinisikan nanti

  /**
   * Override method _createInput yang bertanggung jawab membuat elemen <input type="file">.
   * Kita akan memanggil versi parent-nya (FieldBinaryImage) dan kemudian menambahkan atribut 'capture'.
   * @param {Element} node - Elemen DOM tempat input akan dibuat.
   * @returns {HTMLInputElement} - Elemen input file yang telah dimodifikasi.
   */
  _createInput(node) {
    // Panggil method _createInput dari FieldBinaryImage standar
    const input = super._createInput(node);

    // Tambahkan atribut 'capture' untuk memicu kamera
    // "environment" untuk kamera belakang, "user" untuk kamera depan, atau "" untuk pilihan
    input.setAttribute("capture", "environment");

    // Atribut accept="image/*" biasanya sudah ditambahkan oleh FieldBinaryImage standar,
    // tapi jika ingin memastikan, bisa ditambahkan di sini juga:
    // input.setAttribute("accept", "image/*");

    return input;
  }
}

// Daftarkan widget kustom Anda di registry field Odoo
// Nama 'x_camera_image' akan digunakan di XML view
registry.category("fields").add("x_camera_image", FieldBinaryCameraImage);
