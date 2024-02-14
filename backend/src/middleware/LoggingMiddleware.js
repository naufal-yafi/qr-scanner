const colors = {
  green: "\x1b[32m",
  yellow: "\x1b[33m",
  red: "\x1b[31m",
};

const recolor = (color, text) => {
  return `${color}${text}\x1b[0m`;
};

const dateFormat = (date) => {
  const originalDate = date;
  const dateObject = new Date(originalDate);

  const day = dateObject.getUTCDate().toString().padStart(2, "0");
  const month = (dateObject.getUTCMonth() + 1).toString().padStart(2, "0");
  const year = dateObject.getUTCFullYear().toString();

  const hours = dateObject.getUTCHours().toString().padStart(2, "0");
  const minutes = dateObject.getUTCMinutes().toString().padStart(2, "0");

  return `${day}/${month}/${year} ${hours}:${minutes}`;
};

const LoggingMiddleware = (req, res, next) => {
  const startTimestamp = new Date();
  const method = req.method;
  const url = req.url;

  res.on("finish", () => {
    const endTimestamp = new Date();
    const elapsedTime = endTimestamp - startTimestamp;
    let time;

    if (elapsedTime >= 1000) {
      time = recolor(colors.red, elapsedTime + "ms");
    } else if (elapsedTime >= 500) {
      time = recolor(colors.yellow, elapsedTime + "ms");
    } else {
      time = recolor(colors.green, elapsedTime + "ms");
    }

    console.log(
      `[${dateFormat(startTimestamp.toISOString())}] ${method} ${recolor(
        colors.yellow,
        url
      )} - ${time}`
    );
  });

  next();
};

export default LoggingMiddleware;
