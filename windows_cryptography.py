from ctypes import windll, Structure, c_int, c_char_p, byref
from binascii import unhexlify

crypt_unprotect_data = windll.crypt32.CryptUnprotectData
crypt_binary_to_string = windll.crypt32.CryptBinaryToStringW
"""
	crypt_unprotect_data(
		pDataIn, 	# A pointer to the DataBlob holding the encrypted data.
		ppszDataDescr, 		# Set to None
		pOptionalEntropy, 	# Set to None
		pvReserved, 		# Set to None
		pPromptStruct, 		# Set to None
		dwFlags,  			# Set to None
		pDataOut) 	# A pointer to an empty DataBlob where the output will be
					stored.

	For more information on the function CryptUnprotectData, visit:
	https://msdn.microsoft.com/en-us/library/windows/desktop/aa380882.aspx
"""


# The DataBlob definition is a translation from the C++ code located here:
# https://msdn.microsoft.com/en-us/library/windows/desktop/aa381414.aspx
class DataBlob(Structure):
	_fields_ = [("cbData", c_int), ("pbData", c_char_p)]
	# :cBData: A variable representing the length of the encrypted data.
	# :pbData: A pointer to the encrypted data.


def decrypt_password(hexKey):
	# CryptProtectData encrypts passwords as hexidecimal numbers, they must
	# be converted to binary form before decryption.
	binary_encryption = unhexlify(bytes(hexKey, 'ascii'))
	data_in = DataBlob(len(binary_encryption), c_char_p(binary_encryption))
	data_out = DataBlob()
	if crypt_unprotect_data(byref(data_in), None, None, None, None, None, byref(data_out)):
		return data_out.pbData, data_out.cbData
	else:
		return ""
