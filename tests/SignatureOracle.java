import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.Map;

/** Optional cross-check against the real Java SDK and backend classes, no network. */
public class SignatureOracle {
    public static void main(String[] args) throws Exception {
        JSONObject fixture = JSON.parseObject(Files.readString(Path.of(args[0])));
        String key = fixture.getString("api_key");
        for (Object item : fixture.getJSONArray("vectors")) {
            JSONObject vector = (JSONObject) item;
            Map<String, Object> params = new LinkedHashMap<>(vector.getJSONObject("params"));
            params.remove("sign");
            params.put("version", "1.0");
            params.put("signType", "MD5");
            params.put("reqTime", Long.toString((long) (fixture.getDoubleValue("time_seconds") * 1000)));
            String canonical = com.jeequan.jeepay.util.JeepayKit.getStrSort(params) + "key=" + key;
            String sdk = com.jeequan.jeepay.util.JeepayKit.getSign(params, key);
            String backend = com.jeequan.jeepay.core.utils.JeepayKit.getSign(params, key);
            if (!canonical.equals(vector.getString("canonical")) ||
                    !sdk.equals(vector.getString("sign")) || !backend.equals(sdk)) {
                throw new AssertionError(vector.getString("name") + ": Java oracle mismatch");
            }
            System.out.println("PASS " + vector.getString("name") + " " + sdk);
        }
    }
}
