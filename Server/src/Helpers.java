
public class Helpers {

	public static int packetLength = 516;
	public static int opcodeLength = 4;
	public static int maxByteSize = 255;
	public static byte[] concat(byte[] a, byte[] b) {
    int aLen = a.length;
    int bLen = b.length;
    byte[] c= new byte[aLen+bLen];
    System.arraycopy(a, 0, c, 0, aLen);
    System.arraycopy(b, 0, c, aLen, bLen);
    return c;
 }

}
