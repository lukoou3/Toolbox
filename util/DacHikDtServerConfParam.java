package com.dp.dac.param;

public class DacHikDtServerConfParam
{
	private String webServerIp = "";
	private int webServerPort;
	private String dbIp = "";
	private int dbPort;
	private String dbName = "";	
	private String dbPasswd = "";	
	private boolean enable = false;

	public String getWebServerIp()
	{
		return webServerIp;
	}

	public void setWebServerIp(String webServerIp)
	{
		this.webServerIp = webServerIp;
	}

	public int getWebServerPort()
	{
		return webServerPort;
	}

	public void setWebServerPort(int webServerPort)
	{
		this.webServerPort = webServerPort;
	}

	public String getDbIp()
	{
		return dbIp;
	}

	public void setDbIp(String dbIp)
	{
		this.dbIp = dbIp;
	}

	public int getDbPort()
	{
		return dbPort;
	}

	public void setDbPort(int dbPort)
	{
		this.dbPort = dbPort;
	}

	public String getDbName()
	{
		return dbName;
	}

	public void setDbName(String dbName)
	{
		this.dbName = dbName;
	}

	public String getDbPasswd()
	{
		return dbPasswd;
	}

	public void setDbPasswd(String dbPasswd)
	{
		this.dbPasswd = dbPasswd;
	}

	public boolean isEnable()
	{
		return enable;
	}

	public void setEnable(boolean enable)
	{
		this.enable = enable;
	}	
}

